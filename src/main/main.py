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
WEBCAM_DEVICES = ["video0"] # Add more from USB hub

LOOP_NUM = 0

if __name__ == "__main__":
    while True:
        telemetry = ""
        print("Entering bmp280.py...") if not DIREWOLF_MODE else None
        try:
            telemetry += bmp280.read_sensor()
        except Exception as e:
            print(f"Unable to read from bmp280: {e}") if not DIREWOLF_MODE else None

        print("Entering vfan.py...") if not DIREWOLF_MODE else None
        telemetry += vfan.read_gps()

        if len(telemetry) != 0:
            print(f"Data: {telemetry}") if not DIREWOLF_MODE else None # Send this string to Direwolf
        else:
            print("Unable to collect data.\nRetrying...") if not DIREWOLF_MODE else None

        print("Entering webcam.py...") if not DIREWOLF_MODE else None
        try:
            images_saved = webcam.capture_images(SAVE_DIRECTORY, WEBCAM_DEVICES)
            for i in range(len(images_saved)):
                if i < len(images_saved) - 1:
                    print(f"Image saved at {images_saved[i]}")
                else:
                    print(f"{images_saved[i]} image(s) saved.")
        except Exception as e:
            print(f"Unable to capture image: {e}") if not DIREWOLF_MODE else None

        if DIREWOLF_MODE:
            break
        else:
            time.sleep(TIME_DELAY)
