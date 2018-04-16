
from app.core.bluetooth import bt_controller

if __name__ == '__main__':
    devices = bt_controller.scan()
    for device in devices:
        print("Mac: " + str(device.addr) + ", Name=" + str(device.name))