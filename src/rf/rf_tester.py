from rf_controller import RfController
from rf_signal import RfSignal

signalList = {}


def callback(rf_signal):
    title = input("Name the incoming signal: ")

    if title in signalList:
        signalList[title] = rf_signal


if __name__ == '__main__':
    rf_controller = RfController()
    rf_controller.subscribe(callback)
    while True:
        print("Options: " + str(signalList.keys()))
        option = input("Select option by name: ")

        if not option:
            continue

        signal = signalList[option]
        print("Send RF-Signal: " + str(signal))

        rf_controller.send(signal)
