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

# webcam.py
SAVE_DIRECTORY = "../../images"
WEBCAM_DEVICES = ["video0"]  # Add more devices from USB hub

# aprs.py
CALLSIGN = "KE8ZXE"
SSID = "-11"  # balloon
SAMPLE_RATE = 44100

if __name__ == "__main__":
    ################################
    #                              #
    #        DIREWOLF MODE		   #
    #                              #
    ################################
    if DIREWOLF_MODE:
        telemetry = ""
        try:
            telemetry += bmp280.read_sensor()
        except Exception as e:
            print(f"Unable to read from bmp280: {e}")

        try:
            gps_data = vfan.read_gps()
            telemetry += ",".join(gps_data)
        except Exception as e:
            print(f"Unable to read gps data: {e}")

        if len(telemetry) > 0:
            print(f"Data: {telemetry}")
            try:
                packetAPRS = aprs.create_aprs_packet(CALLSIGN,SSID,telemetry)
                aprs.transmit_audio(packetAPRS, SAMPLE_RATE)
            except Exception as e:
                print(f"Unable to transmit data: {e}")
        else:
            print("Unable to collect data.\nRetrying...")

        try:
            images_saved = webcam.capture_images(SAVE_DIRECTORY,WEBCAM_DEVICES)
        except Exception as e:
            print(f"Unable to capture image: {e}")

        #if len(gps_data) > 0:
            #cur_lat = gps_data[0]
            #cur_long = gps_data[1]
            #try:
                #aprs.update_direwolf_beacon_config(cur_lat,cur_long)
                #aprs.restart_direwolf()
            #except Exception as e:
                #print(f"Unable to update beacon: {e}")

    ############################
    #                          #
    #        DEBUG MODE		   #
    #                          #
    ############################
    elif not DIREWOLF_MODE:
        while True:
            telemetry = ""
            print("Entering bmp280.py...")
            try:
                telemetry += bmp280.read_sensor()
            except Exception as e:
                print(f"Unable to read from bmp280: {e}")

            print("Entering vfan.py...")
            try:
                gps_data = vfan.read_gps()
                telemetry += ",".join(gps_data)
            except Exception as e:
                print(f"Unable to read gps data: {e}")

            if len(telemetry) != 0:
                print(f"Data: {telemetry}")  # Send this string to Direwolf
            else:
                print("Unable to collect data.\nRetrying...")

            print("Entering webcam.py...")
            try:
                images_saved = webcam.capture_images(SAVE_DIRECTORY,WEBCAM_DEVICES)
                for i in range(len(images_saved)):
                    if i < len(images_saved)-1:
                        print(f"Image saved at {images_saved[i]}")
                    else:
                        print(f"{images_saved[i]} image(s) saved.")
            except Exception as e:
                print(f"Unable to capture image: {e}")

            time.sleep(LOOP_TIME_DELAY)
