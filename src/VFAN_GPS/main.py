import gps

def read_gps():
    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    try:
        while True:
            report = session.next()
            if report['class'] == 'TPV':
                if hasattr(report, 'lat') and hasattr(report, 'lon'):
                    latitude = report.lat
                    longitude = report.lon
                    print(f"Latitude: {latitude}, Longitude: {longitude}")

    except KeyboardInterrupt:
        print("\nTerminating GPS reading.")

if __name__ == "__main__":
    read_gps()
