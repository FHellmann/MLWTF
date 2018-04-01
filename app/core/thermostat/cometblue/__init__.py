#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

import logging
import time
import gatt

from .util import decode_str, decode_datetime, encode_datetime, decode_status, encode_status, \
    decode_temperatures, encode_temperatures, decode_battery, decode_lcd_timer, encode_lcd_timer, encode_pin, \
    decode_day, encode_day, decode_holiday, encode_holiday, increase_uuid

_LOGGER = logging.getLogger(__name__)


class CometBlueManager(gatt.DeviceManager):
    def __init__(self, adapter_name):
        super().__init__(adapter_name)

    def make_device(self, mac_address):
        return CometBlue(mac_address = mac_address, manager = self)


class CometBlue(gatt.Device):
    SUPPORTED_VALUES = {
        'device_name': {
            'description': 'device name',
            'uuid': '00002a00-0000-1000-8000-00805f9b34fb',
            'decode': decode_str,
        },

        'model_number': {
            'description': 'model number',
            'uuid': '00002a24-0000-1000-8000-00805f9b34fb',
            'decode': decode_str,
        },

        'firmware_revision': {
            'description': 'firmware revision',
            'uuid': '00002a26-0000-1000-8000-00805f9b34fb',
            'decode': decode_str,
        },

        'software_revision': {
            'description': 'software revision',
            'uuid': '00002a28-0000-1000-8000-00805f9b34fb',
            'decode': decode_str,
        },

        'manufacturer_name': {
            'description': 'manufacturer name',
            'uuid': '00002a29-0000-1000-8000-00805f9b34fb',
            'decode': decode_str,
        },

        'datetime': {
            'description': 'time and date',
            'uuid': '47e9ee01-47e9-11e4-8939-164230d1df67',
            'read_requires_pin': True,
            'decode': decode_datetime,
            'encode': encode_datetime,
        },

        'status': {
            'description': 'status',
            'uuid': '47e9ee2a-47e9-11e4-8939-164230d1df67',
            'read_requires_pin': True,
            'decode': decode_status,
            'encode': encode_status,
        },

        'temperatures': {
            'description': 'temperatures',
            'uuid': '47e9ee2b-47e9-11e4-8939-164230d1df67',
            'read_requires_pin': True,
            'decode': decode_temperatures,
            'encode': encode_temperatures,
        },

        'battery': {
            'description': 'battery charge',
            'uuid': '47e9ee2c-47e9-11e4-8939-164230d1df67',
            'read_requires_pin': True,
            'decode': decode_battery,
        },

        'firmware_revision2': {
            'description': 'firmware revision #2',
            'uuid': '47e9ee2d-47e9-11e4-8939-164230d1df67',
            'read_requires_pin': True,
            'decode': decode_str,
        },

        'lcd_timer': {
            'description': 'LCD timer',
            'uuid': '47e9ee2e-47e9-11e4-8939-164230d1df67',
            'read_requires_pin': True,
            'decode': decode_lcd_timer,
            'encode': encode_lcd_timer,
        },

        'pin': {
            'description': 'PIN',
            'uuid': '47e9ee30-47e9-11e4-8939-164230d1df67',
            'encode': encode_pin,
        },
    }

    SUPPORTED_TABLE_VALUES = {
        'day': {
            'uuid': '47e9ee10-47e9-11e4-8939-164230d1df67',
            'num': 7,
            'read_requires_pin': True,
            'decode': decode_day,
            'encode': encode_day,
        },

        'holiday': {
            'uuid': '47e9ee20-47e9-11e4-8939-164230d1df67',
            'num': 8,
            'read_requires_pin': True,
            'decode': decode_holiday,
            'encode': encode_holiday,
        },
    }

    def _cb_read_value(self, uuid, decode, pin_required):
        if not self.is_connected():
            raise RuntimeError('Not connected')

        if pin_required and (self._pin is None):
            raise RuntimeError('PIN required')

        if pin_required:
            self._cb_wait_pinok()

        if self.aborter():
            raise StopIteration('Operation aborted due to external request')

        _LOGGER.debug('Reading value "%s" from "%s"...', uuid, self.mac_address)

        characteristics_handle = self._cb_chars.get(uuid, None)
        if characteristics_handle is None:
            raise RuntimeError('Handle for uuid "%s" not found, perhaps sync issue?' % uuid)

        value = characteristics_handle.read_value()

        _LOGGER.debug('Read value "%s" from "%s": %r',
                   uuid, self.mac_address, value)
        if len(value.signature) != 1:
            raise RuntimeError('Got more than one value')

        value = bytes(int(byte) for byte in value)
        value = decode(value)
        _LOGGER.debug('Decoded value "%s" from "%s": %r',
                   uuid, self.mac_address, value)
        return value

    def _cb_read_value_n(self, uuid, decode, pin_required, max_n, n):
        if (n < 0) or (n >= max_n):
            raise RuntimeError('Invalid table row number')
        return self._cb_read_value(increase_uuid(uuid, n), decode, pin_required)

    def characteristic_write_value_succeeded(self, characteristic):
        _LOGGER.debug("write for " + characteristic.uuid + " succeeded")
        self._cb_writes[characteristic.uuid] = True

    def characteristic_write_value_failed(self, characteristic, error):
        self._cb_writes[characteristic.uuid] = False
        _LOGGER.error('Value write failed for characteristic "%s" with error "%s"' % (characteristic.uuid, error))

    def _cb_wait_write_result(self, uuid):
        iterations_limit = self._cb_complete_timeout / self._cb_complete_sleep
        i = 0
        while i < iterations_limit and not self.aborter():
            i += 1
            if not self.is_connected():
                raise StopIteration('Device disconnected while waiting for reply')

            if not self._cb_writes.get(uuid, None) is None:
                return self._cb_writes[uuid]
            time.sleep(self._cb_complete_sleep)

        if self.aborter():
            raise StopIteration('Operation aborted due to external request')

        raise StopIteration('Operation has not been completed within timeout')


    def _cb_wait_pinok(self):
        uuid = self.SUPPORTED_VALUES['pin']['uuid']
        if not self._cb_wait_write_result(uuid):
            _LOGGER.debug('Failed to write pin characteristic')
            raise StopIteration('Failed to write pin to device')

    def _cb_write_value(self, uuid, encode, value):
        if not self.is_connected():
            raise RuntimeError('Not connected')

        if self._pin is None:
            raise RuntimeError('PIN required')

        # precaution - glib main loop runs in the same thread as services_discovered,
        # therefore waiting for pin confirmation inside write would cause livelock, as there
        # would be no main loop available for dbus call
        pin_uuid = self.SUPPORTED_VALUES['pin']['uuid']
        if pin_uuid != uuid:
            self._cb_wait_pinok()

        _LOGGER.debug('Writing value "%s" to "%s": %r...',
                   uuid, self.mac_address, value)

        characteristics_handle = self._cb_chars.get(uuid, None)
        if characteristics_handle is None:
            if self._cb_chars:
                raise NotImplementedError('Device does not offer characteristics with uuid "%s", required to fulfill the request' % uuid)
            else:
                raise RuntimeError('Handle for characteristics uuid "%s" not found, perhaps sync issue?' % uuid)

        self._cb_writes[uuid] = None
        value = encode(value)
        characteristics_handle.write_value(value)

        if not self.blocking:
            _LOGGER.debug('Assuming successfull write "%s" to "%s": %r', uuid, self.mac_address, value)
            return

        if self._cb_wait_write_result(uuid):
            _LOGGER.debug('Confirmed write value "%s" to "%s": %r', uuid, self.mac_address, value)
            return

        _LOGGER.debug('Write failed for "%s" to "%s": %r', uuid, self.mac_address, value)


    def _cb_write_value_n(self, uuid, encode, max_n, n, value):
        if (n < 0) or (n >= max_n):
            raise RuntimeError('Invalid table row number')
        return self._cb_write_value(increase_uuid(uuid, n), encode, value)

    @property
    def blocking(self):
        return self._blocking

    @blocking.setter
    def blocking(self, blocking):
        self._blocking = blocking

    @property
    def aborter(self):
        return self._aborter

    @aborter.setter
    def aborter(self, aborter):
        if aborter is None:
            aborter = lambda: False
        self._aborter = aborter

    @property
    def pin(self):
        return self._pin

    @pin.setter
    def pin(self, _pin):
        self._pin = _pin

    def __init__(self, mac_address, manager, pin=None, aborter=None):
        super().__init__(mac_address, manager)

        self._cb_chars = None
        self._cb_writes = {}
        self._pin = pin
        # for manual connect + disconnect vs. __enter__ vs. __exit__
        self._enter_nesting = 0
        self._cb_enter_managed_connection = True
        self._cb_setup_methods()
        self._blocking = True
        self.aborter = aborter
        self._cb_complete_timeout = 60
        self._cb_complete_sleep = 0.050

    def _cb_setup_methods(self):
        for val_name, val_conf in six.iteritems(self.SUPPORTED_VALUES):
            if 'decode' in val_conf:
                setattr(
                        self,
                        'get_' + val_name,
                        functools.partial(
                                self._cb_read_value,
                                str(val_conf['uuid']),
                                val_conf['decode'],
                                val_conf.get('read_requires_pin', False)))
            if 'encode' in val_conf:
                setattr(
                        self,
                        'set_' + val_name,
                        functools.partial(
                                self._cb_write_value,
                                str(val_conf['uuid']),
                                val_conf['encode']))

        for val_name, val_conf in six.iteritems(self.SUPPORTED_TABLE_VALUES):
            if 'decode' in val_conf:
                setattr(
                        self,
                        'get_' + val_name,
                        functools.partial(
                                self._cb_read_value_n,
                                str(val_conf['uuid']),
                                val_conf['decode'],
                                val_conf.get('read_requires_pin', False),
                                val_conf['num']))
            if 'encode' in val_conf:
                setattr(
                        self,
                        'set_' + val_name,
                        functools.partial(
                                self._cb_write_value_n,
                                str(val_conf['uuid']),
                                val_conf['encode'],
                                val_conf['num']))

    def __str__(self):
        return \
            "device_" + self.alias() \
            + "@" + self.mac_address + "_[" \
            + ("connected" if self.is_connected() else "disconnected") \
            + ", " \
            + ("services resolved" if self.is_services_resolved() else "pending service resolution") + "]"

    def enumerate_unhandled_characteristics(self):
        handled = []
        for _, simple in self.SUPPORTED_VALUES.items():
            handled.append(simple['uuid'])
        for _, tabbed in self.SUPPORTED_TABLE_VALUES.items():
            for i in range(tabbed['num']):
                handled.append(increase_uuid(tabbed['uuid'], i))

        unhandled_characteristics = []
        for characteristics in self._cb_chars.keys():
            if characteristics not in handled:
                unhandled_characteristics.append(characteristics)
        return unhandled_characteristics

    def services_resolved(self):
        super().services_resolved()
        self._cb_chars = dict(
                (str(characteristics_handle.uuid), characteristics_handle)
                for service_handle in self.services
                for characteristics_handle in service_handle.characteristics )

        _LOGGER.debug('Discovered characteristics for "%s": %r',
                   self.mac_address, self._cb_chars.keys())

        if self._pin is not None:
            try:
                self.blocking = False
                self.set_pin(self._pin)
            except RuntimeError as exc:
                raise RuntimeError('Invalid PIN', exc)
            finally:
                self.blocking = True

        unhandled_characteristics = self.enumerate_unhandled_characteristics()
        if unhandled_characteristics:
            _LOGGER.info('Unknown characteristics discovered on "%s": %r',
                self.mac_address, unhandled_characteristics)


    def __enter__(self):
        self._enter_nesting += 1
        if not self.is_connected():
            self.connect()

        self.attempt_to_get_ready()
        if not self.ready():
            raise RuntimeError("Unable to connect & resolve the device")

        return self

    def connect(self):
        # if connect() is called before __enter__, make it not managed
        if self._enter_nesting == 0:
            self._cb_enter_managed_connection = False

        _LOGGER.info('Connecting to device "%s"...', self.mac_address)
        super().connect()

        if not self.is_connected():
            raise RuntimeError('Failed to connect the device')

    def attempt_to_get_ready(self):
        iterations_limit = self._cb_complete_timeout / self._cb_complete_sleep
        i = 0
        while not self.ready() and i < iterations_limit:
                i += 1
                time.sleep(self._cb_complete_sleep)
        return self.ready()

    def ready(self):
        return self.is_connected() and self.is_services_resolved() and bool(self._cb_chars)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._enter_nesting -= 1

        if self._enter_nesting == 0 and self._cb_enter_managed_connection:
            self.disconnect()

    def disconnect(self):
        if not self.is_connected():
            return

        _LOGGER.info('Disconnecting from device "%s"...', self.mac_address)
        try:
            super().disconnect()
            _LOGGER.info('Disconnected from device "%s"', self.mac_address)
            self._cb_chars = None
            self._cb_writes = {}
        except:
            _LOGGER.error('Failed disconnect from device "%s", considering disconnected anyway', self.mac_address)

    def get_days(self):
        return list(map(self.get_day, range(7)))

    def get_holidays(self):
        return list(map(self.get_holiday, range(8)))

    def backup(self):
        _LOGGER.info('Saving all supported values from "%s"...', self.mac_address)

        data = {}

        for val_name, val_conf in six.iteritems(self.SUPPORTED_VALUES):
            if ('decode' not in val_conf) or ('encode' not in val_conf):
                # Skip read-only or write-only value.
                continue
            if val_name in ('datetime', ):
                # Restoring this from backup makes no sense.
                continue

            data[val_name] = getattr(self, 'get_' + val_name)()

        for val_name in 'days', 'holidays':
            data[val_name] = getattr(self, 'get_' + val_name)()

        _LOGGER.info('All supported values from "%s" saved', self.mac_address)

        return data

    def set_days(self, value):
        for day_n, day in zip(itertools.count(), value):
            self.set_day(day_n, day)

    def set_holidays(self, value):
        for holiday_n, holiday in zip(itertools.count(), value):
            self.set_holiday(holiday_n, holiday)

    def restore(self, data):
        _LOGGER.info('Restoring values from backup for "%s"...', self.mac_address)
        _LOGGER.debug('Backup data: %r', data)

        for val_name, val_data in six.iteritems(data):
            getattr(self, 'set_' + val_name)(val_data)

        if 'datetime' not in data:
            self.set_datetime(datetime.datetime.now())

        _LOGGER.info('Values from backup for "%s" successfully restored', self.mac_address)