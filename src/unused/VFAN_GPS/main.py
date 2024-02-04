from gps import gps, WATCH_ENABLE
import time

def read_gps():
    # print("Entering read_gps function")

    try:
        # Connect to the local GPSD daemon
        session = gps(mode=WATCH_ENABLE)

        report = session.next()
        if report['class'] == 'TPV':
            if 'lat' in report and 'lon' in report and 'alt' in report:
                latitude = report.lat
                longitude = report.lon
                altitude = report.alt
                # Latitude, Longitude, Altitude (m)
                gps_output = f"{latitude},{longitude},{altitude:0.0f}"
                return gps_output
            
    except Exception as e:
        print(f"An error occurred: {e}")


