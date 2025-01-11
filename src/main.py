import bmp280
import vfan
import time
import webcam
import aprs

# main.py
DIREWOLF_MODE = True  # Includes status print statements
LOOP_TIME_DELAY = 10  # Delay in seconds of main loop

# bmp280.py->wifi.py
CUTOFF_ALTITUDE = 1524  # Altitude (in meters) where wifi is turned off

# vfan.py
GPS_DEVICE = "ttyACM0"

# webcam.py
RESOLUTION = "1920x1080"
SKIPPED_FRAMES = 10
CAPTURE_DELAY = 2
CAPTURED_FRAMES = 2
SAVE_DIRECTORY = "../media/images"
WEBCAM_DEVICES = ["video0"]  # Add more devices from USB hub

# aprs.py
CALLSIGN = "KE8ZXE"
SSID = "11"
BAUD_RATE = 1200
SAMPLE_RATE = 48000

if __name__ == "__main__":

    ##################################################
    #                                                #                  
    #                  DIREWOLF MODE                 #
    #                                                #
    ##################################################

    if DIREWOLF_MODE:
        # Initializes data to an empty dict
        data_list = {

        try:
            # Collect data from bmp280
            bmp280_dict = bmp280.read_sensor()

            # Add bmp280 data to data_list
            data_list["BMP280"] = bmp280_dict

        except Exception as e:
            print(f"Unable to read from bmp280: {e}")

        try:
            # Collect data from VFAN GPS
            gps_dict = vfan.read_gps(GPS_DEVICE)
            
            # Add VFAN GPS data to data_list
            data_list["VFAN"] = gps_dict

        except Exception as e:
            print(f"Unable to read gps data: {e}")

        if len(data_list.keys()) > 0:
            # Print the telemetry string
            for entry in data_list:
                for data in entry.keys():
                    print(f"Data: {data}:{entry[data]}")

            try:
                # Create an APRS packet from telemetry
                packetAPRS = aprs.create_aprs_packet(CALLSIGN, SSID, data_list)
                
                # Generate AFSK audio for the APRS packet
                audio_data = aprs.generate_afsk(packetAPRS, BAUD_RATE, SAMPLE_RATE)
                
                # Transmit the APRS packet
                aprs.transmit_audio(audio_data, SAMPLE_RATE)

            except Exception as e:
                print(f"Unable to transmit data: {e}")

        else:
            print("Unable to collect data.")

        try:
            # Capture and save image(s) using webcam
            images_saved = webcam.capture_images(RESOLUTION, SKIPPED_FRAMES, CAPTURE_DELAY,
                                                  CAPTURED_FRAMES, SAVE_DIRECTORY, WEBCAM_DEVICES)
        except Exception as e:
            print(f"Unable to capture image: {e}")

    ##################################################
    #                                                #                  
    #                   DEBUG MODE                   #
    #                                                #
    ##################################################
            
    elif not DIREWOLF_MODE:
        while True:
            # Initializes data to an empty list
            data_list = []

            # Delimiter for data string
            delimiter = ","
            
            print("Entering bmp280.py...")

            try:
                # Collect data from bmp280
                bmp280_data = bmp280.read_sensor()

                for data in bmp280_data:
                    # Add bmp280 data to data_list
                    data_list.append(data)

            except Exception as e:
                print(f"Unable to read from bmp280: {e}")

            print("Entering vfan.py...")

            try:
                # Collect data from VFAN GPS
                gps_data = vfan.read_gps(GPS_DEVICE)

                for data in gps_data:
                    # Add VFAN GPS data to data_list
                    data_list.append(data)

            except Exception as e:
                print(f"Unable to read gps data: {e}")

            if len(data_list) > 0:
                # Convert data_list to telemetry string
                telemetry = delimiter.join(data_list)

                # Print the telemetry string
                print(f"Data: {telemetry}")

            else:
                print("Unable to collect data.\nRetrying...")

            print("Entering webcam.py...")

            try:
                # Capture and save image(s) using webcam
                images_saved = webcam.capture_images(RESOLUTION, SKIPPED_FRAMES, CAPTURE_DELAY,
                                                     CAPTURED_FRAMES,SAVE_DIRECTORY, WEBCAM_DEVICES)
                for i in range(len(images_saved)):
                    # Print number of images/location
                    if type(images_saved[i]) == int:
                        print(f"{images_saved[i]} image(s) saved.")   
                                            
                    else:
                        print(f"Image saved at {images_saved[i]}")   

            except Exception as e:
                print(f"Unable to capture image: {e}")

            # Waits a specified time before looping again
            time.sleep(LOOP_TIME_DELAY)
