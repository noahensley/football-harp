import bmp280
import vfan
import time
import webcam

# main.py
DEBUG_MODE = True # Includes status print statements
LOOP_TIME_DELAY = 10  # Delay in seconds of main loop

# bmp280.py->wifi.py
CUTOFF_ALTITUDE = 1524  # Altitude (in meters) where wifi is turned off

# webcam.py
SAVE_DIRECTORY = "../../images"
WEBCAM_DEVICES = ["video0"] # Add more devices from USB hub

LOOP_NUM = 0

if __name__ == "__main__":
    while DEBUG_MODE:
        telemetry = ""
        print("Entering bmp280.py...")
        try:
            telemetry += bmp280.read_sensor()
        except Exception as e:
            print(f"Unable to read from bmp280: {e}")

        print("Entering vfan.py...")
        telemetry += vfan.read_gps()

        if len(telemetry) != 0:
            print(f"Data: {telemetry}") # Send this string to Direwolf
        else:
            print("Unable to collect data.\nRetrying...")

        print("Entering webcam.py...")
        try:
            images_saved = webcam.capture_images(SAVE_DIRECTORY, WEBCAM_DEVICES)
            for i in range(len(images_saved)):
                if i < len(images_saved) - 1:
                    print(f"Image saved at {images_saved[i]}")
                else:
                    print(f"{images_saved[i]} image(s) saved.")
        except Exception as e:
            print(f"Unable to capture image: {e}")

        time.sleep(LOOP_TIME_DELAY)            
            
    if not DEBUG_MODE:
        telemetry = ""
        try:
            telemetry += bmp280.read_sensor()
        except Exception as e:
            print(f"Unable to read from bmp280: {e}")

        telemetry += vfan.read_gps()

        if len(telemetry) != 0:
            print(f"Data: {telemetry}") # Send this string to Direwolf
        else:
            print("Unable to collect data.\nRetrying...")

        try:
            images_saved = webcam.capture_images(SAVE_DIRECTORY, WEBCAM_DEVICES)
        except Exception as e:
            print(f"Unable to capture image: {e}")
