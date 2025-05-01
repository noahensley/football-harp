import time
import webcam
import os

# webcam.py
RESOLUTION = "1920x1080"
SAVE_DIRECTORY = "/home/n8ssu/images"
WEBCAM_DEVICES = ["video0","video2",'video4']  # Add more devices from USB hub
DELAY = 1 # seconds between captures
FREECAP = .05 # kill if disk is full - % free

while True:
    statvfs = os.statvfs(SAVE_DIRECTORY)
    free = statvfs.f_bfree / statvfs.f_blocks
    print("Disk Used", statvfs.f_bfree, statvfs.f_blocks, round(free,3))
    if free > FREECAP:
        images_saved = webcam.ffmpeg_capture_images(RESOLUTION, SAVE_DIRECTORY, WEBCAM_DEVICES)
    else:
        print("Disk Fill - Image capture stopped.")
    time.sleep(DELAY)
