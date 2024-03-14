import subprocess
from gps import gps, WATCH_ENABLE

def read_gps():
    gps_output = []  # Default value

    try:
        # Check if the GPS device is present
        device_check = subprocess.check_output(["ls", "/dev"]).decode("utf-8")
        if "ttyACM0" in device_check:  # Change "ttyUSB0" to your GPS device name
            # GPS device is present, connect to the local GPSD daemon
            session = gps(mode=WATCH_ENABLE)
    
            while True:
                report = session.next()
                if report['class'] == 'TPV':
                    if report.lat != 'n/a' and report.lon != 'n/a' and report.alt != 'n/a':
                        latitude = report.lat
                        longitude = report.lon
                        altitude = report.alt
                        # Latitude, Longitude, Altitude (m)
                        gps_output.append(str(latitude))
                        gps_output.append(str(longitude))
                        gps_output.append(str(round(altitude,1)))
                        return gps_output  # Return GPS data if available
        else:
            print("GPS device not found")
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        return gps_output  # Return default value if unable to connect or retrieve GPS data
