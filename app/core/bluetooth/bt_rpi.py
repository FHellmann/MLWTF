"""
A simple wrapper for bluepy's btle.Connection.
Handles Connection duties (reconnecting etc.) transparently.
"""
import logging
import codecs

from bluepy import btle

from .models import BluetoothDevice

DEFAULT_TIMEOUT = 1

_LOGGER = logging.getLogger(__name__)


class BTLEConnection(btle.DefaultDelegate):
    """Representation of a BTLE Connection."""

    def __init__(self, device: BluetoothDevice):
        """Initialize the connection."""
        btle.DefaultDelegate.__init__(self)

        self._conn = None
        self._device = device
        self._callbacks = {}

    def __enter__(self):
        """
        Context manager __enter__ for connecting the device
        :rtype: btle.Peripheral
        :return:
        """
        self._conn = btle.Peripheral()
        self._conn.withDelegate(self)
        _LOGGER.debug("Trying to connect to %s", self._device.mac)
        try:
            self._conn.connect(self._device.mac)
        except btle.BTLEException as ex:
            _LOGGER.debug("Unable to connect to the device %s, retrying: %s", self._device.mac, ex)
            try:
                self._conn.connect(self._device.mac)
            except Exception as ex2:
                _LOGGER.debug("Second connection try to %s failed: %s", self._device.mac, ex2)
                raise

        _LOGGER.debug("Connected to %s", self._device.mac)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            self._conn.disconnect()
            self._conn = None

    def handleNotification(self, handle, data):
        """Handle Callback from a Bluetooth (GATT) request."""
        _LOGGER.debug("Got notification from %s: %s", handle, codecs.encode(data, 'hex'))
        if handle in self._callbacks:
            self._callbacks[handle](data)

    @property
    def device(self):
        return self._device

    def set_callback(self, handle, function):
        """Set the callback for a Notification handle. It will be called with the parameter data, which is binary."""
        self._callbacks[handle] = function

    def make_request(self, handle, value, timeout=DEFAULT_TIMEOUT, with_response=True):
        """Write a GATT Command without callback - not utf-8."""
        try:
            with self:
                _LOGGER.debug("Writing %s to %s with with_response=%s", codecs.encode(value, 'hex'), handle, with_response)
                self._conn.writeCharacteristic(handle, value, withResponse=with_response)
                if timeout:
                    _LOGGER.debug("Waiting for notifications for %s", timeout)
                    self._conn.waitForNotifications(timeout)
        except btle.BTLEException as ex:
            _LOGGER.debug("Got exception from bluepy while making a request: %s", ex)
            raise


class BluetoothConnector(object):
    def __init__(self):
        self.scanner = btle.Scanner()
        self.curr_conn = None
        self.curr_device = None
        self.handle = "btle_handle_my-smart-home"

    def scan(self):
        devices = self.scanner.scan(passive=True)
        result = []

        for dev in devices:
            result.append(BluetoothDevice(dev.addr))
            #print("Device %s (%s), RSSI=%d dB", dev.addr, dev.addrType, dev.rssi)
            #for (adtype, desc, value) in dev.getScanData():
            #    print("  %s = %s", desc, value)
        return result

    def connect(self, device : BluetoothDevice, callback_function):
        self.curr_conn = BTLEConnection(device.mac)
        self.curr_conn.set_callback(self.handle, callback_function)

    def disconnect(self):
        self.curr_conn = None

    def send(self, value):
        self.curr_conn.make_request(self.handle, value)
