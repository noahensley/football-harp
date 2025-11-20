import bmp280
import ublox
import time
import webcam
import aprs_tx
import telem

# Import/centralize macros, one configuration file (config.py)
from config import DEBUG_MODE, LOGGING_MODE

from config import LOOP_TIME_DELAY

from config import GPS_MAX_ATTEMPTS, GPS_TIMEOUT

from config import RESOLUTION, SKIPPED_FRAMES, CAPTURE_DELAY, CAPTURED_FRAMES
from config import WEBCAM_DEVICES

from config import CALLSIGN, SSID


if __name__ == "__main__":

    while True:
        # Initializes data list to empty dict
        data_list = {}

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
            # Collect data from UBLOX GPS
            gps_dict = ublox.poll_gps(max_no_fix_cycles=GPS_MAX_ATTEMPTS, timeout_seconds=GPS_TIMEOUT)
            # Add UBLOX GPS data to data_list
            data_list["UBLOX"] = gps_dict

        except IOError as e:
            print("ERROR:", e)

        except Exception as e:
            print("ERROR:", e)

        # Print the telemetry string
        if DEBUG_MODE:
            for sensor in data_list:
                for data in data_list[sensor].keys():
                    print(f"Data: {data}:{data_list[sensor][data]}")

        packetAPRS = ""
        try:
            # Create an APRS packet from telemetry
            packetAPRS = aprs_tx.create_aprs_packet(CALLSIGN, SSID, data_list, message="TEST BEACON")
            
            # Transmit the APRS packet
            aprs_tx.transmit_via_direwolf_kiss(packetAPRS)

        except Exception as e:
            print("ERROR:", e)
	
        try:
            if LOGGING_MODE:
                telem.log_data(data=packetAPRS)

        except Exception as e:
            print("ERROR:", e)

        try:
            if LOGGING_MODE:
                images_saved = webcam.capture_images(RESOLUTION, SKIPPED_FRAMES, CAPTURE_DELAY,
                                                        CAPTURED_FRAMES, WEBCAM_DEVICES)
        except Exception as e:
            print("ERROR:", e)
            
        print("=" * 68)
        time.sleep(LOOP_TIME_DELAY)
