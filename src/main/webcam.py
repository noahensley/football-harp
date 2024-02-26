import os
import subprocess
from datetime import datetime

def capture_image(file_path, device_path):
    try:
        # Formats the current date/time to a string
        formatted_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Creates a custom image filepath using the current date/time
        unique_image_file_path = os.path.join(file_path, f"{formatted_datetime}.jpg")

        # Constructs an fswebcam command using the unique filepath
        cmd = f"fswebcam -r 1920x1080 -p YUYV -S 10 -D 2 -F 2 -d {device_path} {unique_image_file_path} > /dev/null 2>&1"

        subprocess.run(cmd, shell=True)

        return unique_image_file_path

    except subprocess.CalledProcessError as e:
        print(f"Unable to execute command: {e}")
        return None
    except Exception as e:
        print(f"An error has occurred: {e}")
        return None
