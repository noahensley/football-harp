import bmp280
import vfan
import time

DIREWOLF_MODE = False
TIME_DELAY = 10 # in seconds

LOOP_NUM = 0

if __name__ == "__main__":
    while True:
        telemetry = ""
        try:
            # print("Entering bmp280.py...")
            telemetry += bmp280.read_sensor()
        except Exception as e:
            print(f"Unable to read from bmp280: {e}")
            
        try:    
            # print("Entering vfan.py...")
            telemetry += vfan.read_gps()
        except Exception as e:
            print(f"Unable to read from GPS: {e}")
            
        if len(telemetry) != 0:
            print(telemetry)
        else:
            print("Unable to collect data.\nRetrying...")
            
        if DIREWOLF_MODE:
            break
        else:
            time.sleep(TIME_DELAY)
