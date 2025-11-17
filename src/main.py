import bmp280
import vfan
import time
import webcam
import aprs_tx
import telem

# Move these macros to config.py (currently debug.py)
# Import macros
# Import utils.log_telemetry_data (refactor)

# debug.py
from debug import DEBUG_MODE

# main.py
LOOP_TIME_DELAY = 20  # Delay in seconds of main loop

# bmp280.py->wifi.py
CUTOFF_ALTITUDE = 1524  # Altitude (in meters) where wifi is turned off

# vfan.py
GPS_DEVICE = "ttyAMA0"
GPS_MAX_ATTEMPTS = 2
GPS_TIMEOUT = 2

# webcam.py
RESOLUTION = "1920x1080"
SKIPPED_FRAMES = 10
CAPTURE_DELAY = 2
CAPTURED_FRAMES = 2
#SAVE_DIRECTORY = "../media/images"
WEBCAM_DEVICES = ["video0", "video2", "video4"]  # Each USB hub webcam takes two video* devices
                                                 # (i.e. Camera 1 => video0/video1)

# aprs.py
CALLSIGN = "KE8ZXE"
SSID = "11"
BAUD_RATE = 1200
SAMPLE_RATE = 48000


if __name__ == "__main__":

    while True:
        # Initializes data to an empty dict
        # dummy data
        data_list = {"VFAN": {"Latitude": 10.18, "Longitude": 789.2}}

        try:
            # Collect data from bmp280
            bmp280_dict = bmp280.read_sensor()

            # Add bmp280 data to data_list
            data_list["BMP280"] = bmp280_dict

        except IOError as e:
            print("ERROR:", "Missing BMP280 device.")

        except Exception as e:
            print("ERROR:", "Error reading from BMP280 device.")

        try:
            # Collect data from VFAN GPS
            gps_dict = vfan.read_gps(GPS_DEVICE, max_attempts=GPS_MAX_ATTEMPTS, timeout=GPS_TIMEOUT)
            # Add VFAN GPS data to data_list
            data_list["VFAN"] = gps_dict

        except IOError as e:
            print("ERROR:", e)

        except Exception as e:
            print("ERROR:", e)

        # Print the telemetry string
        if DEBUG_MODE:
            for sensor in data_list:
                for data in data_list[sensor].keys():
                    print(f"Data: {data}:{data_list[sensor][data]}")

        try:
            # Create an APRS packet from telemetry
            packetAPRS = aprs_tx.create_aprs_packet(CALLSIGN, SSID, data_list, message="TEST BEACON")
            
            # Transmit the APRS packet
            aprs_tx.transmit_via_direwolf_kiss(packetAPRS)

        except Exception as e:
            print("ERROR:", e)
	
        try:
            pass
            #telem.log_data(data=packetAPRS)

        except Exception as e:
            print("ERROR:", e)

        try:
            # Capture and save image(s) using webcam
            pass
            #images_saved = webcam.capture_images(RESOLUTION, SKIPPED_FRAMES, CAPTURE_DELAY,
            #                                      CAPTURED_FRAMES, WEBCAM_DEVICES)
        except Exception as e:
            print("ERROR:", e)
            
        print("=" * 68)
        time.sleep(LOOP_TIME_DELAY)
