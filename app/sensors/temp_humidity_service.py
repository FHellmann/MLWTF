from enum import Enum


class Type(Enum):
    DHT11 = 1
    DHT22 = 2


class DHTException(Exception):
    def __init__(self, mess):
        self.message = mess


DHT_HANDSHAKE_ERROR = -1
DHT_TIMEOUT_ERROR = -2
DHT_CHECKSUM_ERROR = -3
DHT_INPUT_ERROR = -4
DHT_INIT_ERROR = -5
DHT_OK = 0


def sensor_read(sensor_type, gpio_pin):
    result, humidity, temperature = MyPyDHT.dht_driver._dht_read(sensor_type.value, gpio_pin)

    if result != DHT_OK:
        if result == DHT_HANDSHAKE_ERROR:
            error_mess = "An error occurred during the handshake with the sensor!"
        elif result == DHT_TIMEOUT_ERROR:
            error_mess = "A timeout occurred while attempting to read the sensor!"
        elif result == DHT_CHECKSUM_ERROR:
            error_mess = "The checksum verification of sensors' data failed!"
        elif result == DHT_INIT_ERROR:
            error_mess = "An error occurred while initializing the GPIO ports"
        else:
            # result == DHT_INPUT_ERROR
            error_mess = "Invalid data passed as arguments to the sensor!"
        raise DHTException(error_mess)

    return round(humidity, 2), round(temperature, 2)
