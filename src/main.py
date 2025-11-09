import bmp280
import vfan
import time
import webcam
import aprs_tx

# main.py
LOOP_TIME_DELAY = 10  # Delay in seconds of main loop

# bmp280.py->wifi.py
CUTOFF_ALTITUDE = 1524  # Altitude (in meters) where wifi is turned off

# vfan.py
GPS_DEVICE = "ttyACM0"
GPS_MAX_ATTEMPTS = 2
GPS_TIMEOUT = 2

# webcam.py
RESOLUTION = "1920x1080"
SKIPPED_FRAMES = 10
CAPTURE_DELAY = 2
CAPTURED_FRAMES = 2
SAVE_DIRECTORY = "../media/images"
WEBCAM_DEVICES = ["video0", "video2", "video4"]  # Each USB hub webcam takes two video* devices
                                                 # (i.e. Camera 1 => video0/video1)

# aprs.py
CALLSIGN = "KE8ZXE"
SSID = "11"
BAUD_RATE = 1200
SAMPLE_RATE = 48000


if __name__ == "__main__":

    while True:
        #th_recieve_cmd.start()

        # Initializes data to an empty dict
        data_list = {}

        try:
            # Collect data from bmp280
            bmp280_dict = bmp280.read_sensor()

            # Add bmp280 data to data_list
            data_list["BMP280"] = bmp280_dict

        except IOError as e:
            print("Unable to connect to bmp280: ", e)

        except Exception as e:
            print("Unable to read from bmp280: ", e)

        try:
            # Collect data from VFAN GPS
            gps_dict = vfan.read_gps(GPS_DEVICE, max_attempts=GPS_MAX_ATTEMPTS, timeout=GPS_TIMEOUT)
            
            # Add VFAN GPS data to data_list
            data_list["VFAN"] = gps_dict

        except IOError as e:
            print("Unable to connect to VFAN GPS: ", e)

        except Exception as e:
            print("Unable to read gps data: ", e)

        if len(data_list.keys()) > 0:
            # Print the telemetry string
            for sensor in data_list:
                for data in data_list[sensor].keys():
                    print(f"Data: {data}:{data_list[sensor][data]}")

            try:
                # Create an APRS packet from telemetry
                packetAPRS = aprs_tx.create_aprs_packet(CALLSIGN, SSID, data_list)
                
                # Generate AFSK audio for the APRS packet
                audio_data = aprs_tx.generate_afsk(packetAPRS, BAUD_RATE, SAMPLE_RATE)
                
                # Transmit the APRS packet
                aprs_tx.transmit_audio(audio_data, SAMPLE_RATE)

            except Exception as e:
                print("Unable to transmit APRS data: ", e)

        else:
            print("No data to transmit.")

        try:
            # Capture and save image(s) using webcam
            images_saved = webcam.capture_images(RESOLUTION, SKIPPED_FRAMES, CAPTURE_DELAY,
                                                  CAPTURED_FRAMES, SAVE_DIRECTORY, WEBCAM_DEVICES)
        except Exception as e:
            print(f"Unable to capture image: {e}")
            
        print("=" * 68)
        time.sleep(LOOP_TIME_DELAY)
    
#th_recieve_cmd.join()