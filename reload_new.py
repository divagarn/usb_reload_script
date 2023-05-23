# launch with file path
import pyudev
import subprocess
import roslaunch


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
        subprocess.run(['sudo', 'udevadm', 'control', '--reload-rules'], check=True)
        subprocess.run(['sudo', 'udevadm', 'trigger'], check=True)
        print("USB rules reloaded successfully.")
    except subprocess.CalledProcessError as e:
        print("Error reloading USB rules:", e)


def launch_master(launch_file_path):
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)

    launch = roslaunch.parent.ROSLaunchParent(uuid, [launch_file_path])
    launch.start()
    print("ROS master launched.")

    # Keep the program running until ROS master is shut down
    while launch.is_alive():
        pass


def main():
    # List of USB vendor IDs and product IDs to check
    device_list = [
        ('VendorID1', 'ProductID1'),
        ('VendorID2', 'ProductID2'),
        ('VendorID3', 'ProductID3')
    ]

    try:
        if check_usb_devices(device_list):
            print("All USB devices are available.")
        else:
            print("Some USB devices are not available.")
            reload_usb_rule()

            if check_usb_devices(device_list):
                print("All USB devices are now available.")
                launch_file_path = '/path/to/master.launch'  # Replace with the actual file path
                launch_master(launch_file_path)
            else:
                print("USB devices are still not available after reloading USB rules.")
    except pyudev.DeviceNotFoundError as e:
        print("Error accessing USB devices:", e)


if __name__ == '__main__':
    main()
