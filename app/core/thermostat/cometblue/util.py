#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging
import datetime
import struct
import uuid as uuid_module

from app.core.thermostat.models import StructPacking, Holiday, Status, Temperature

_LOGGER = logging.getLogger(__name__)

_STATUS_BITMASKS = {
    'childlock': 0x80,
    'manual_mode': 0x1,
    'adapting': 0x400,
    'not_ready': 0x200,
    'installing': 0x400 | 0x200 | 0x100,
    'motor_moving': 0x100,
    'antifrost_activated': 0x10,
    'satisfied': 0x80000,
    'low_battery': 0x800
}


def encode_pin(pin):
    return struct.pack(StructPacking.PIN.value, pin)


def decode_datetime(value):
    mi, ho, da, mo, ye = struct.unpack(StructPacking.DATETIME.value, value)
    return datetime.datetime(
            year=ye + 2000,
            month=mo,
            day=da,
            hour=ho,
            minute=mi)


def encode_datetime(dt):
    if dt.year < 2000:
        raise RuntimeError('Invalid year')
    return struct.pack(
            StructPacking.DATETIME.value,
            dt.minute,
            dt.hour,
            dt.day,
            dt.month,
            dt.year - 2000)


def decode_status(value):
    state_dword = struct.unpack('<I', value + b'\x00')[0]

    report = {}
    masked_out = 0
    for key, mask in _STATUS_BITMASKS.items():
        report[key] = bool(state_dword & mask == mask)
        masked_out |= mask

    return Status(state_as_dword=state_dword, unused_bits=state_dword & ~masked_out)


def encode_status(status : Status):
    status_dword = 0
    for key, state in status.items():
        if not state:
            continue

        if not key in _STATUS_BITMASKS:
            _LOGGER.error('Unknown flag ' + key)
            continue

        status_dword |= _STATUS_BITMASKS[key]

    status = struct.pack('<I', status_dword)
    # downcast to 3 bytes
    return struct.pack(StructPacking.STATUS.value, *[int(byte) for byte in status[:3]])


def decode_temperatures(value):
    cur_temp, manual_temp, target_low, target_high, offset_temp, \
            window_open_detect, window_open_minutes = struct.unpack(
                StructPacking.TEMPERATURES.value, value)
    return Temperature(
        current_temp=cur_temp / 2.0,
        manual_temp=manual_temp / 2.0,
        target_temp_l=target_low / 2.0,
        target_temp_h=target_high / 2.0,
        offset_temp=offset_temp / 2.0,
        window_open_detection=window_open_detect,
        window_open_minutes=window_open_minutes
    )


def _temp_float_to_int(value : float):
    if value is None:
        return -128  # do not change setting
    return int(value * 2.0)


def _temp_int_to_int(value : int):
    if value is None:
        return -128  # do not change setting
    return value


def encode_temperatures(temperature : Temperature):
    return struct.pack(
            StructPacking.TEMPERATURES.value,
            -128,  # current_temp
            _temp_float_to_int(temperature.manual_temp),
            _temp_float_to_int(temperature.target_temp_l),
            _temp_float_to_int(temperature.target_temp_h),
            _temp_float_to_int(temperature.offset_temp),
            _temp_int_to_int(temperature.window_open_detection),
            _temp_int_to_int(temperature.window_open_minutes))


def decode_str(value):
    return value.decode()


def decode_battery(value):
    value = struct.unpack(StructPacking.BATTERY.value, value)[0]
    if value == 255:
        return None
    return value


def decode_lcd_timer(value):
    preload, current = struct.unpack(StructPacking.LCD_TIMER.value, value)
    return {
        'preload': preload,
        'current': current,
    }


def encode_lcd_timer(lcd_timer):
    return struct.pack(
            StructPacking.LCD_TIMER.value,
            lcd_timer['preload'],
            0)


class _day_period_cmp(object):
    def __init__(self, period):
        self.period = period

    def __lt__(self, other):
        if self.period['start'] is None:
            return False
        if other.period['start'] is None:
            return True
        return self.period['start'] < other.period['start']

    def __gt__(self, other):
        return other < self

    def __eq__(self, other):
        return self.period['start'] == other.period['start']

    def __le__(self, other):
        return self == other or self < other

    def __ge__(self, other):
        return self == other or self > other

    def __ne__(self, other):
        return not self == other


def decode_day(value):
    max_raw_time = ((23 * 60) + 59) / 10

    raw_time_values = list(struct.unpack(StructPacking.DAY.value, value))
    day = []
    while raw_time_values:
        raw_start = raw_time_values.pop(0)
        raw_end = raw_time_values.pop(0)

        if raw_end > max_raw_time:
            start = None
            end = None
        else:
            if raw_start > max_raw_time:
                start = datetime.time()
            else:
                raw_start *= 10
                start = datetime.time(hour=raw_start // 60,
                                      minute=raw_start % 60)

            if raw_end > max_raw_time:
                end = datetime.time(23, 59, 59)
            else:
                raw_end *= 10
                end = datetime.time(hour=raw_end // 60,
                                    minute=raw_end % 60)

        if start == end:
            day.append({
                'start': None,
                'end': None,
            })
        else:
            day.append({
                'start': start,
                'end': end,
            })

    day.sort(key=_day_period_cmp)

    return day


def encode_day(periods):
    if len(periods) > 4:
        raise RuntimeError('Too many periods')
    periods = list(periods)
    periods.extend([dict(start=None, end=None)] * (4 - len(periods)))

    values = []
    for period in periods:
        if period['start'] is None:
            start = 255
            end = 255
        else:
            start = (period['start'].hour * 60 + period['start'].minute) // 10
            end = (period['end'].hour * 60 + period['end'].minute) // 10

        if start == 0:
            start = 255
        if end == 0:
            end = 255

        values.append(start)
        values.append(end)

    return struct.pack(StructPacking.DAY.value, *values)


def decode_holiday(value):
    ho_start, da_start, mo_start, ye_start, \
            ho_end, da_end, mo_end, ye_end, \
            temp = struct.unpack(StructPacking.HOLIDAY.value, value)

    if (ho_start > 23) or (ho_end > 23) \
            or (da_start > 31) or (da_end > 31) \
            or (da_start < 1) or (da_end < 1) \
            or (mo_start > 12) or (mo_end > 12) \
            or (mo_start < 1) or (mo_end < 1) \
            or (ye_start > 99) or (ye_end > 99) \
            or (temp == -128):
        start = None
        end = None
        temp = None
    else:
        start = datetime.datetime(
                year=ye_start + 2000,
                month=mo_start,
                day=da_start,
                hour=ho_start)
        end = datetime.datetime(
                year=ye_end + 2000,
                month=mo_end,
                day=da_end,
                hour=ho_end)
        temp = temp / 2.0

    return Holiday(start, end, temp)


def encode_holiday(holiday : Holiday):
    if not(holiday.is_active()):
        return struct.pack(StructPacking.HOLIDAY.value,
                           128, 128, 128, 128, 128, 128, 128, 128, -128)

    if (holiday.start.year < 2000) or (holiday.end.year < 2000):
        raise RuntimeError('Invalid year')

    return struct.pack(
            StructPacking.HOLIDAY.value,
            holiday.start.hour,
            holiday.start.day,
            holiday.start.month,
            holiday.start.year - 2000,
            holiday.end.hour,
            holiday.end.day,
            holiday.end.month,
            holiday.end.year - 2000,
            _temp_float_to_int(holiday.temperature))


def increase_uuid(uuid_str, n):
    uuid_obj = uuid_module.UUID(uuid_str)
    uuid_fields = list(uuid_obj.fields)
    uuid_fields[0] += n
    return str(uuid_module.UUID(fields=uuid_fields))
