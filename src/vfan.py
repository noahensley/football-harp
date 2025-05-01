import subprocess
from gps import gps, WATCH_ENABLE
import time

from debug import DEBUG_MODE

def read_gps(gps_device, max_attempts=5, timeout=3):
    """
    Connects to a USB VFAN GPS device and attempts to read latitude, longitude, 
    and altitude data. Makes a limited number of attempts before returning.
    
    Parameters:
        gps_device (str): The GPS device found in the /dev folder (e.g. "ttyACM0").
        max_attempts (int): Maximum number of attempts to read GPS data.
        timeout (int): Max wait time for GPS data

    Returns:
        dict: A dictionary of latitude, longitude, and altitude readings, or empty dict if no data.
    """
    
    if DEBUG_MODE: 
        print("Reading GPS...")
        
    # Output initially empty
    gps_output_data = {}

    try:
        # Get the list of devices in /dev directory
        device_list = subprocess.check_output(["ls", "/dev"]).decode("utf-8")

        # Check if the GPS device path is present in the list of devices
        if gps_device in device_list:
            # GPS device (ttyACM0) is present, establish connection
            session = gps(mode=WATCH_ENABLE)
            
            # Make a limited number of attempts to get GPS data
            for attempt in range(1, max_attempts + 1):
                if DEBUG_MODE:
                    print(f"GPS read attempt {attempt}/{max_attempts}")               

                # Set a short timeout for this attempt
                if session.waiting(timeout):  # Wait for data (false if no data)
                    report = session.next()
                    print("Data received.  Checking...")
                else:
                    print("Timeout exceeded. ",end="")
                    if attempt == max_attempts:
                        print("Exiting...")
                    else:
                        print("Retrying...")         
                    continue
                
                if hasattr(report, 'class') and report['class'] == 'TPV':
                    # Check if report has the required attributes
                    if hasattr(report, 'lat') and hasattr(report, 'lon') and hasattr(report, 'alt'):
                        # Ensures latitude, longitude, and altitude are valid
                        if report.lat != 'n/a' and report.lon != 'n/a' and report.alt != 'n/a':
                            # Adds data to data dictionary
                            gps_output_data["Latitude"] = str(report.lat)
                            gps_output_data["Longitude"] = str(report.lon)
                            gps_output_data["Altitude"] = str(round(report.alt, 1))
                            
                            if DEBUG_MODE:
                                print("GOOD")
                            
                            return gps_output_data
                        
                    else:
                        # Required key was missing, error
                        if DEBUG_MODE:
                            print("ERROR: MISSING REQUIRED DATA")
                else:
                    #Likely communicating with wrong device
                    if DEBUG_MODE:
                        print("ERROR: DEVICE NOT TPV")
                
                # Brief pause before next attempt
                time.sleep(0.5)
                
        else:
            # GPS device was not found in the device list
            raise IOError(f"GPS device '{gps_device}' not found")

    except Exception as e:
        raise Exception("Unexpected error occurred: ", e)
            
    finally:
        # Close the session if it was opened
        if 'session' in locals():
            try:
                session.close()
            except:
                pass