import time
import signal
from gps import gps, WATCH_ENABLE

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Timeout occurred while initializing GPS session")

def read_gps():
    gps_output = ""

    try:
        # Set a timeout for connecting to the local GPSD daemon
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(10)  # Set the timeout value (in seconds)

        # Connect to the local GPSD daemon
        session = gps(mode=WATCH_ENABLE)
        signal.alarm(0)  # Cancel the timeout

        while True:
            report = session.next()
            if report['class'] == 'TPV':
                if report.lat != 'n/a' and report.lon != 'n/a' and report.alt != 'n/a':
                    latitude = report.lat
                    longitude = report.lon
                    altitude = report.alt
                    # Latitude, Longitude, Altitude (m)
                    gps_output = f"{latitude},{longitude},{altitude:0.0f}"
                    return gps_output  # Return GPS data if available
                else:
                    raise ValueError("Latitude, longitude, or altitude is 'n/a'")
        
    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
    except ValueError as e:
        print(f"ValueError occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        signal.alarm(0)  # Ensure alarm is canceled even if an exception occurs
        return gps_output  # Return default value if unable to connect or retrieve GPS data
