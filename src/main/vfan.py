from gps import gps, WATCH_ENABLE
import time

GPS_TIMEOUT = 10  # Timeout in seconds

def read_gps():
    # print("Entering read_gps function")
    gps_output = "NO GPS DATA"
    start_time = time.time()

    try:
        # Connect to the local GPSD daemon
        session = gps(mode=WATCH_ENABLE)

        while True:
            report = session.next()
            if report['class'] == 'TPV':
                if 'lat' in report and 'lon' in report and 'alt' in report:
                    latitude = report.lat
                    longitude = report.lon
                    altitude = report.alt
                    # Latitude, Longitude, Altitude (m)
                    gps_output = f"{latitude},{longitude},{altitude:0.0f}"

                    elapsed_time = time.time() - start_time
                    # print(f"Elapsed Time: {elapsed_time:.2f}s, GPS Data: {gps_output}")

                    if elapsed_time > GPS_TIMEOUT:
                        break
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    # Default return statement
    return gps_output
