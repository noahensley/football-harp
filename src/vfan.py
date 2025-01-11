import subprocess
from gps import gps, WATCH_ENABLE

def read_gps(gps_device):
    """
    Connects to a USB VFAN GPS device and reads latitude, longitude, and altitude data.
    
    Parameters:
        gps_device (str): The GPS device found in the /dev folder (e.g. "ttyACM0").

    Returns:
        list[str]: A list of latitude, longitude, and altitude readings.
    """
    # Output initially empty
    #gps_output_data = []
    gps_output_data = {}

    try:
        # Get the list of devices in /dev directory
        device_list = subprocess.check_output(["ls", "/dev"]).decode("utf-8")

        # Check if the GPS device path is present in the list of devices
        if gps_device in device_list:
            # GPS device is present, establish connection
            session = gps(mode=WATCH_ENABLE)   

            while True:
                # Grabs data from the GPS
                report = session.next()

                if report['class'] == 'TPV':
                    # Ensures latitude, longitude, and altitude are valid
                    if report.lat != 'n/a' and report.lon != 'n/a' and report.alt != 'n/a':
                        # Adds data to data list
                        #gps_output_data.append(str(report.lat))
                        #gps_output_data.append(str(report.lon))
                        # Rounds altitude (m) to 1 decimal place
                        #gps_output_data.append(str(round(report.alt,1)))
                        
                        # Uses a dict instead
                        gps_output_data["Latitude"] = str(report.lat)
                        gps_output_data["Longitude"] = str(report.lon)
                        gps_output_data["Altitude"] = str(round(report.alt, 1))
                        
                        # Return GPS data
                        return gps_output_data
        else:
            # GPS device was not found in the device list
            print("GPS device not found")

    except Exception as e:
        print(f"An error occurred: {e}")  
            
    finally:
        # Return default value if unable to connect or retrieve GPS data
        return gps_output_data
