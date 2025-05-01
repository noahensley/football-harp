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
            # GPS device is present, establish connection
            session = gps(mode=WATCH_ENABLE)
            
            # Make a limited number of attempts to get GPS data
            for attempt in range(1, max_attempts + 1):
                if DEBUG_MODE:
                    print(f"GPS read attempt {attempt+1}/{max_attempts}")
                
                # Try to grab data from the GPS
                try:
                    # Set a short timeout for this attempt
                    session.waiting(3)  # Wait up to 3 seconds for data
                    report = session.next()
                    
                    if report['class'] == 'TPV':
                        # Check if report has the required attributes
                        if hasattr(report, 'lat') and hasattr(report, 'lon') and hasattr(report, 'alt'):
                            # Ensures latitude, longitude, and altitude are valid
                            if report.lat != 'n/a' and report.lon != 'n/a' and report.alt != 'n/a':
                                # Adds data to data dictionary
                                gps_output_data["Latitude"] = str(report.lat)
                                gps_output_data["Longitude"] = str(report.lon)
                                gps_output_data["Altitude"] = str(round(report.alt, 1))
                                
                                if DEBUG_MODE:
                                    print("GPS data successfully read")
                                
                                return gps_output_data
                
                except (KeyError, AttributeError) as e:
                    # Log the issue but continue to next attempt
                    if DEBUG_MODE:
                        print(f"GPS data read issue: {e}")
                
                # Brief pause before next attempt
                time.sleep(0.5)
                
        else:
            # GPS device was not found in the device list
            if DEBUG_MODE:
                print(f"GPS device '{gps_device}' not found in /dev")
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
        
        # Return the data (may be empty)
        return gps_output_data