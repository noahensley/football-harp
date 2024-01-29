from gps import gps, WATCH_ENABLE
import time

DIREWOLF_MODE = True # False = continuous readings

TIME_DELAY = 2 # in seconds

def read_gps():
    print("Entering read_gps function")

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
                    print(f"{latitude},{longitude},{altitude:0.0f}")

                    if DIREWOLF_MODE:
                        break
            else:
                time.sleep(TIME_DELAY)

    except KeyboardInterrupt:
        print("\nTerminating GPS reading.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Running the script")
    read_gps()
