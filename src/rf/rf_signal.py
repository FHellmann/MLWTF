#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""


class RfSignal:
    def __init__(self, time, rx_code, rx_pulselength, rx_protocol):
        self.time = time
        self.rx_code = rx_code
        self.rx_pulselength = rx_pulselength
        self.rx_protocol = rx_protocol

    def get_time(self):
        return self.time

    def get_code(self):
        return self.rx_code

    def get_pulselength(self):
        return self.rx_pulselength

    def get_protocol(self):
        return self.rx_protocol

    def __str__(self):
        return "RF-Signal(time=" + str(self.get_time()) + ", code=" + str(self.get_code()) + \
               ", pulselength=" + str(self.get_pulselength()) + ", protocol=" + str(self.get_protocol()) + ")"
