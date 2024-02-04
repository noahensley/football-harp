import bmp280
import vfan
import time

DIREWOLF_MODE = False
TIME_DELAY = 1  # in seconds

if __name__ == "__main__":
    while True:
        telemetry = bmp280.read_sensor()
        telemetry += vfan.read_gps()
        print(telemetry)
        if DIREWOLF_MODE:
            break
        else:
            time.sleep(TIME_DELAY)
