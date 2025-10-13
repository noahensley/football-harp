import os
import subprocess
from datetime import datetime
from typing import List, Union



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


def capture_images(img_res, file_path, webcam_devices) -> List[Union[str, int]]:
    """
    Uses fswebcam to save an image of specified resolution to a specified filepath.

    Parameters:
        img_res (str): The desired resolution for the image in form "****x****" (e.g. "1920x1080").
        file_path (str): The directory where the images will be saved (relative to /main).
        webcam_devices (list[str]): A list of webcam USB devices to iterate through (e.g. "video0").

    Returns:
        Union[str, int]: A list of the filepaths of the capture images, and the number of saved images.
        The number of saved images is always the item in the last index.


    """

    SKIPPED_FRAMES = 3
    CAPTURE_DELAY = 0
    CAPTURED_FRAMES = 2
    DELAY = 1 # seconds between captures

    # The number of images saved
    num_images_saved = 0

    # A list of the saved image filepaths (initially empty)
    generated_image_paths = []

    # Captures an image from each webcam
    for webcam in webcam_devices:
        # Ensures webcam is connected
        if not webcam_connected(webcam):
            raise RuntimeError("Webcam disconnected or invalid device path.")  
             
        # Formats the current date/time to a string
        formatted_datetime = datetime.now().strftime("%Y%m%d%H%M%S%f")
        
        # Creates a unique image filepath using the current date/time
        unique_image_file_path = os.path.join(file_path, f"{webcam}_{formatted_datetime}.jpg")

        # Adds unique filepath to a list of filepaths
        generated_image_paths.append(unique_image_file_path)

        # Constructs an fswebcam command using the the function arguments
        cmd = (
            f"fswebcam -r {img_res} "
            f"-S {SKIPPED_FRAMES} -D {CAPTURE_DELAY} -F {CAPTURED_FRAMES} "
            f"-d /dev/{webcam} {unique_image_file_path} "
            "> /dev/null"
        )
        print(cmd)

        # Checks that the images were captured successfully
        if (subprocess.run(cmd, shell=True)).returncode == 0:
            # Increments the number of successful captures
            num_images_saved += 1            

    # Adds success count to the end of the list to be returned
    generated_image_paths.append(str(num_images_saved))

    # Returns list of image filepaths (and the number saved)
    return generated_image_paths



def ffmpeg_capture_images(img_res, file_path, webcam_devices) -> List[Union[str, int]]:
    """
    Uses fswebcam to save an image of specified resolution to a specified filepath.

    Parameters:
        img_res (str): The desired resolution for the image in form "****x****" (e.g. "1920x1080").
        file_path (str): The directory where the images will be saved (relative to /main).
        webcam_devices (list[str]): A list of webcam USB devices to iterate through (e.g. "video0").

    Returns:
        Union[str, int]: A list of the filepaths of the capture images, and the number of saved images.
        The number of saved images is always the item in the last index.


    """

    num_images_saved = 0
    generated_image_paths = []

    for webcam in webcam_devices:
        if not webcam_connected(webcam):
            raise RuntimeError("Webcam disconnected or invalid device path.")  
             
        formatted_datetime = datetime.now().strftime("%Y%m%d%H%M%S%f")
        unique_image_file_path = os.path.join(file_path, f"{webcam}_{formatted_datetime}.jpg")
        generated_image_paths.append(unique_image_file_path)

        cmd = (
            f"ffmpeg "
            f" -f video4linux2"
            f" -i /dev/{webcam}"
            f" -s {img_res}"
            f" -ss 2"
            f" -frames 1"
            f" {unique_image_file_path}"
            
        )
        print(cmd)

        if (subprocess.run(cmd, shell=True)).returncode == 0:
            num_images_saved += 1            

    generated_image_paths.append(str(num_images_saved))

    return generated_image_paths

