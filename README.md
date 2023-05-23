# USB Device Monitor

This is a Python script that monitors USB devices and checks if a specific list of USB devices is connected. It uses the `pyudev` library to interact with the Linux device manager (`udev`) and `rospy` library for ROS (Robot Operating System) functionality.

## Requirements

- Python 3.x
- `pyudev` library (`pip install pyudev`)
- ROS (Robot Operating System)

## Usage

1. Clone the repository or download the script `usb_device_monitor.py`.

2. Install the required dependencies by running the following command:
```bash
pip install pyudev
```


3. Make sure you have ROS installed on your system.

4. Modify the `device_list` variable in the `main()` function of `usb_device_monitor.py` script to contain the desired USB vendor IDs and product IDs to check. Add or remove entries as necessary.

5. Run the script with appropriate privileges:
```bash
python usb_device_monitor.py
```



6. The script will initialize a ROS node, monitor USB devices, and check if all the specified USB devices are connected. It will print the status of the USB devices and update the ROS parameter `/usb_available_status` accordingly.

7. If all USB devices are found, the script will exit with status code 0. If some devices are missing, it will attempt to reload the USB rules and check again. If the devices are still not available, it will exit with status code 1.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Author

This script was authored by [divagarn](https://github.com/divagarn).


