import os
import subprocess
from datetime import datetime

def is_webcam_connected(webcam):
    # Get the list of devices in /dev directory
    device_list = subprocess.check_output(["ls", "/dev"]).decode("utf-8")
    
    # Check if the device path is present in the list of devices
    if webcam in device_list:
        return True
    else:
        return False

def capture_images(file_path, webcam_devices):
    success_count = 0
    unique_paths = []
    for webcam in webcam_devices:
        # Ensures webcam is connected
        if not is_webcam_connected(webcam):
            raise RuntimeError("Webcam disconnected or invalid device path.")
        
        success_count += 1
        # Formats the current date/time to a string
        formatted_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Creates a custom image filepath using the current date/time
        unique_image_file_path = os.path.join(file_path, f"{formatted_datetime}.jpg")

        # Constructs an fswebcam command using the unique filepath
        cmd = f"fswebcam -r 1920x1080 -p YUYV -S 10 -D 2 -F 2 -d /dev/{webcam} {unique_image_file_path} > /dev/null 2>&1"
        
        unique_paths.append(unique_image_file_path)

        subprocess.run(cmd, shell=True)
    
    unique_paths.append(str(success_count))
    
    return unique_paths
