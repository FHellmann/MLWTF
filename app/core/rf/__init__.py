#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from . import rf_rpi
from ..gpio import RaspberryPi3 as GPIO_PI
from app.database import RfSignal, db_add


def send(signal):
    _rx_device.disable_rx()
    success = _tx_device.tx_code(signal)
    _rx_device.enable_rx()
    return success


def _convert(signal):
    return RfSignal(
        code=signal.code,
        pulse_length=signal.pulse_length,
        bit_length=signal.bit_length,
        sync_high=signal.protocol.sync_high,
        sync_low=signal.protocol.sync_low,
        zero_high=signal.protocol.zero_high,
        zero_low=signal.protocol.zero_low,
        one_high=signal.protocol.one_high,
        one_low=signal.protocol.one_low
    )


def _receive(signal):
    db_add(_convert(signal))


_rx_device = rf_rpi.Device(GPIO_PI.GPIO_27.value)
_rx_device.enable_rx()
_rx_device.add_rx_listener(_receive)

_tx_device = rf_rpi.Device(GPIO_PI.GPIO_17.value)
_tx_device.enable_tx()
