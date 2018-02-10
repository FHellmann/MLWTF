import time

from rf_controller import RfController
from rf_signal import RfSignal

signalList = {}


def callback(rf_signal):
    if str(rf_signal.get_code()) not in signalList:
        signalList[str(rf_signal.get_code())] = rf_signal


if __name__ == '__main__':
    rf_controller = RfController()
    rf_controller.subscribe(callback)
    while True:
        while len(signalList.keys()) == 0:
            time.sleep(0.01)

        print("Options: " + str(signalList.keys()))
        option = input("Select option by number: ")

        if not option:
            continue

        signal = signalList[option]
        print("Send RF-Signal: " + str(signal))

        rf_controller.send(signal)
