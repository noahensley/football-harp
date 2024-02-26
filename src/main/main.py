import bmp280
import vfan
import time
import webcam

# main.py
DIREWOLF_MODE = False
TIME_DELAY = 10  # in seconds

# bmp280.py->wifi.py
CUTOFF_ALTITUDE = 1524  # meters

# webcam.py
SAVE_DIRECTORY = "../../images"
WEBCAM_DEVICE_PATH = "video0"

LOOP_NUM = 0

if __name__ == "__main__":
    while True:
        telemetry = ""
        print("Entering bmp280.py...") if DIREWOLF_MODE is False else None
        try:
            telemetry += bmp280.read_sensor()
        except Exception as e:
            print(f"Unable to read from bmp280: {e}") if DIREWOLF_MODE is False else None

        print("Entering vfan.py...") if DIREWOLF_MODE is False else None
        telemetry += vfan.read_gps()

        if len(telemetry) != 0:
            print(f"Data: {telemetry}") if DIREWOLF_MODE is False else None # Send this string to Direwolf
        else:
            print("Unable to collect data.\nRetrying...") if DIREWOLF_MODE is False else None

        print("Entering webcam.py...") if DIREWOLF_MODE is False else None
        try:           
            image_filepath = webcam.capture_image(SAVE_DIRECTORY, WEBCAM_DEVICE_PATH)
            print(f"Image captured and saved at {image_filepath}") if DIREWOLF_MODE is False else None
        except Exception as e:
            print(f"Unable to capture image: {e}") if DIREWOLF_MODE is False else None

        if DIREWOLF_MODE:
            break
        else:
            time.sleep(TIME_DELAY)
