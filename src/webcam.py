import os
import subprocess
from datetime import datetime
from typing import List, Union

from debug import DEBUG_MODE

from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
IMAGE_DIR = ROOT_DIR / "data/images/"
# Make a default image save location

def webcam_connected(webcam):
    """
    Checks the /dev directory for a specified webcam device path.

    Parameters:
    webcam (str): The webcam device found in the /dev folder (e.g. "video0").

    Returns:
        bool: True if the webcam device is found.
        bool: False if the webcam device is not found.
    """
    # Get the list of devices in /dev directory
    device_list = subprocess.check_output(["ls", "/dev"]).decode("utf-8")

    # Check if the webcam device path is present in the list of devices
    if webcam in device_list:
        return True
    else:
        return False

def capture_images(img_res, num_skip, cap_delay, num_cap, webcam_devices, file_path=IMAGE_DIR) -> List[Union[str, int]]:
    """
    Uses fswebcam to save an image of specified resolution to a specified filepath.

    Parameters:
        img_res (str): The desired resolution for the image in form "****x****" (e.g. "1920x1080").
        num_skip (int): The number of frames to skip before capturing.
        cap_delay (int): The delay before capturing an image (in seconds).
        num_cap (int): The number of frames to capture.
        file_path (str): The directory where the images will be saved (relative to /main).
        webcam_devices (list[str]): A list of webcam USB devices to iterate through (e.g. "video0").

    Returns:
        Union[str, int]: A list of the filepaths of the capture images, and the number of saved images.
        The number of saved images is always the item in the last index.
    """
    print(f"[WEBCAM] Capturing {len(webcam_devices)} images...", end="")
    
    # The number of images saved
    num_images_saved = 0

    # A list of the saved image filepaths (initially empty)
    generated_image_paths = []

    # Captures an image from each webcam
    for webcam in webcam_devices:
        # Ensures webcam is connected
        if not webcam_connected(webcam):
            raise IOError("Webcam disconnected or invalid device path.")

        try:  
            # Formats the current date/time to a string
            formatted_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            # Creates a unique image filepath using the current date/time
            unique_image_file_path = os.path.join(file_path, f"{formatted_datetime}.jpg")

            # Adds unique filepath to a list of filepaths
            generated_image_paths.append(unique_image_file_path)

            # Constructs an fswebcam command using the the function arguments
            cmd = (
                f"fswebcam --quiet "
                f"-r {img_res} -p YUYV "
                f"-S {num_skip} -D {cap_delay} -F {num_cap} "
                f"-d /dev/{webcam} {unique_image_file_path} "
                "> /dev/null"
            )

            # Checks that the images were captured successfully
            if (subprocess.run(cmd, shell=True)).returncode == 0:
                # Increments the number of successful captures
                num_images_saved += 1
                if DEBUG_MODE:
                    print(f"Saved image to '{unique_image_file_path}'.")
            else:
                raise Exception("Unable to resolve fswebcam command for ", unique_image_file_path)

        except Exception as e:
            raise Exception("Unable to capture image on" + webcam + "device: ", e)

    # Adds success count to the end of the list to be returned
    generated_image_paths.append(str(num_images_saved))

    # Returns list of image filepaths (and the number saved)
    if num_images_saved > 0:
        print("DONE")
    return generated_image_paths
