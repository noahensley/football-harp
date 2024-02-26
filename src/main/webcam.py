import os
import subprocess
from datetime import datetime

def is_webcam_connected(device_path):
    # Get the list of devices in /dev directory
    device_list = subprocess.check_output(["ls", "/dev"]).decode("utf-8")
    
    # Check if the device path is present in the list of devices
    if device_path in device_list:
        return True
    else:
        return False

def capture_image(file_path, device_path):
    # Ensures webcam is connected
    if not is_webcam_connected(device_path):
        raise RuntimeError("Webcam disconnected or invalid device path.")
        
    # Formats the current date/time to a string
    formatted_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Creates a custom image filepath using the current date/time
    unique_image_file_path = os.path.join(file_path, f"{formatted_datetime}.jpg")

    # Constructs an fswebcam command using the unique filepath
    cmd = f"fswebcam -r 1920x1080 -p YUYV -S 10 -D 2 -F 2 -d /dev/{device_path} {unique_image_file_path} > /dev/null 2>&1"

    subprocess.run(cmd, shell=True)

    return unique_image_file_path
