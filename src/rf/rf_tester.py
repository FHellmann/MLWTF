import time
import cmd

from rf_controller import RfController
from rf_signal import RfSignal

signalList = []


def callback(rf_signal):
    exists = False
    for x in range(0, len(signalList)):
        if signalList[x].get_code() == rf_signal.get_code() & \
                signalList[x].get_pulselength() == rf_signal.get_pulselength() & \
                signalList[x].get_protocol() == rf_signal.get_protocol():
            exists = True

    if not exists:
        signalList.append(rf_signal)


if __name__ == '__main__':
    print("Welcome to RF Tester")
    rf_controller = RfController()
    rf_controller.subscribe(callback)
    while True:
        print("Waiting for RF-Signals...")
        while len(signalList) > 1:
            time.sleep(0.01)

        print("RF-Signals detected: " + str(signalList))
        number = int(input("Choose a RF-Signal to be send by entering the number: "))

        signal = signalList[number]
        print("Send RF-Signal: " + str(signal))

        rf_controller.send(signal)
