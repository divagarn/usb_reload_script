import pyudev
import subprocess

def check_usb_device(vendor_id, product_id):
    context = pyudev.Context()
    usb_devices = list(context.list_devices(subsystem='usb'))
    
    for device in usb_devices:
        if device.get('ID_VENDOR_ID') == vendor_id and device.get('ID_MODEL_ID') == product_id:
            return True
    
    return False

def reload_usb_rule():
    subprocess.run(['sudo', 'udevadm', 'control', '--reload-rules'])
    subprocess.run(['sudo', 'udevadm', 'trigger'])
    
def main():
    # USB vendor ID and product ID to check
    vendor_id = '04ca'  # Replace with the actual vendor ID 04ca:00bd
    product_id = '00bd'  # Replace with the actual product ID
    
    if check_usb_device(vendor_id, product_id):
        print("USB device is available.")
    else:
        print("USB device is not available. Reloading USB rules...")
        reload_usb_rule()
    
if __name__ == '__main__':
    main()
	
