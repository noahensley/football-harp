import os
import subprocess
from datetime import datetime

def is_webcam_connected(webcam):
    """Checks the /dev directory for a specified
    webcam device path."""
    # Get the list of devices in /dev directory
    device_list = subprocess.check_output(["ls", "/dev"]).decode("utf-8")   
    # Check if the webcam device path is present in the list of devices
    if webcam in device_list:
        return True
    else:
        return False

def capture_images(resolution, num_skip, delay, num_cap, file_path, webcam_devices):
    """Uses fswebcam to save an image of specified resolution
    to a specified filepath."""
    # The number of images saved
    num_saved = 0
    # A list of the saved image filepaths
    unique_paths = []
    # Captures an image from each webcam
    for webcam in webcam_devices:
        # Ensures webcam is connected
        if not is_webcam_connected(webcam):
            raise RuntimeError("Webcam disconnected or invalid device path.")       
        # Formats the current date/time to a string
        formatted_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Creates a unique image filepath using the current date/time
        unique_image_file_path = os.path.join(file_path, f"{formatted_datetime}.jpg")
        # Adds unique filepath to a list of filepaths
        unique_paths.append(unique_image_file_path)
        # Constructs an fswebcam command using the the function arguments
        cmd = (
            f"fswebcam -r {resolution} -p YUYV "
            f"-S {num_skip} -D {delay} -F {num_cap} "
            f"-d /dev/{webcam} {unique_image_file_path} "
            "> /dev/null"
        )
        # Checks that the images were captured successfully
        if (subprocess.run(cmd, shell=True)).returncode == 0:
            # Increments the number of successful captures
            num_saved += 1            
    # Adds success count to the end of the list to be returned
    unique_paths.append(str(num_saved))
    # Returns list of image filepaths (and the number saved)
    return unique_paths
