import os
import subprocess
from datetime import datetime

SAVE_DIRECTORY = "../../images"
WEBCAM_DEVICE_PATH = "/dev/video0"

def capture_image(file_path,device_path):
    # Formats the current date/time to a string
    formatted_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Creates a custome image filepath using the current date/time
    unique_image_file_path = os.path.join(file_path, f"{formatted_datetime}.jpg")
    
    # Constructs an fswebcam command using the unique filepath
    cmd = f"fswebcam -r 1920x1080 -p YUYV -S 10 -D 2 -F 2 -d {device_path} {unique_image_file_path}"
    
    subprocess.run(cmd, shell=True)
    
    return unique_image_file_path

if __name__ == "__main__":
    captured_image_path = capture_image(SAVE_DIRECTORY,WEBCAM_DEVICE_PATH)
    
    # print("Image captured and saved at:", captured_image_path)
