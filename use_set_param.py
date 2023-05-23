__author__ = 'divagar'
import pyudev
import rospy
import signal
import os
import sys


def check_usb_devices(device_list):
    context = pyudev.Context()
    usb_devices = list(context.list_devices(subsystem='usb'))

    for device in usb_devices:
        device_id = (device.get('ID_VENDOR_ID'), device.get('ID_MODEL_ID'))
        if device_id in device_list:
            device_list.remove(device_id)

    return len(device_list) == 0


def reload_usb_rule():
    try:
        os.system('sudo udevadm control --reload-rules')
        os.system('sudo udevadm trigger')
        print("USB rules reloaded successfully.")
    except Exception as e:
        print("Error reloading USB rules:", e)


def signal_handler(sig, frame):
    print("Keyboard interrupt detected. Exiting...")
    rospy.signal_shutdown("Keyboard interrupt")
    sys.exit(0)


def main():
    # List of USB vendor IDs and product IDs to check
    device_list = [
        ('VendorID1', 'ProductID1'),
        ('VendorID2', 'ProductID2'),
        ('VendorID3', 'ProductID3')
    ]

    rospy.init_node('usb_device_monitor')
    signal.signal(signal.SIGINT, signal_handler)

    if check_usb_devices(device_list):
        print("All USB devices are available.")
        rospy.set_param('/usb_available_status', 1)
        sys.exit(0)
    else:
        print("Some USB devices are not available.")
        reload_usb_rule()

        if check_usb_devices(device_list):
            print("All USB devices are now available.")
            rospy.set_param('/usb_available_status', 1)
            sys.exit(0)
        else:
            print("USB devices are still not available after reloading USB rules.")
            rospy.set_param('/usb_available_status', 0)  
            sys.exit(0)


if __name__ == '__main__':
    main()
