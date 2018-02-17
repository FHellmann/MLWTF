from enum import Enum


class RaspberryPi3(Enum):
    VOLT1_3_3 = 1
    VOLT1_5_0 = 2
    GPIO_2_SDA = 3
    VOLT2_5_0 = 4
    GPIO_3_SCL = 5
    GND1 = 6
    GPIO_4_GPCLK0 = 7
    GPIO_14_TXD = 8
    GND2 = 9
    GPIO_15_RXD = 10
    GPIO_17 = 11
    GPIO_18 = 12
    GPIO_27 = 13
    GND3 = 14
    GPIO_22 = 15
    GPIO_23 = 16
    VOLT2_3_3 = 17
    GPIO_24 = 18
    GPIO_10_MOSI = 19
    GND4 = 20
    GPIO_9_MISO = 21
    GPIO_25 = 22
    GPIO_11_SCLK = 23
    GPIO_8_CE0 = 24
    GND5 = 25
    GPIO_7_CE1 = 26
    ID_SD = 27
    ID_SC = 28
    GPIO_5 = 29
    GND6 = 30
    GPIO_6 = 31
    GPIO_12 = 32
    GPIO_13 = 33
    GND7 = 34
    GPIO_19 = 35
    GPIO_16 = 36
    GPIO_26 = 37
    GPIO_20 = 38
    GND8 = 39
    GPIO_21 = 40


class ArduinoNano(Enum):
    GPIO_RX = 1
    GPIO_DTR_HASH = 2
    GPIO_RTS_HASH = 3
    GPIO_VCCIO = 4
    GPIO_RXD = 5
    GPIO_RI_HASH = 6
    GND1 = 7
    GPIO_NC1 = 8
    GPIO_DSR_HASH = 9
    GPIO_DCD_HASH = 10
    GPIO_CTS_HASH = 11
    GPIO_CBUS4 = 12
    GPIO_CBUS2 = 13
    GPIO_CBUS3 = 14
    GPIO_USBDP = 15
    GPIO_USBDM = 16
    VOLT_3_3_OUT = 17
    GND2 = 18
    RESET_HASH = 19
    VCC = 20
    GND3 = 21
    GPIO_CBUS1 = 22
    GPIO_CBUS0 = 23
    GPIO_NC2 = 24
    GPIO_AGND = 25
    GPIO_TEST = 26
    GPIO_OSCI = 27
    GPIO_OSC0 = 28
