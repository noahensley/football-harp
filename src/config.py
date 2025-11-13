# Make this file a configuration file named 'config.py'
# Incorporate with main script
DEBUG_MODE = False  # Includes status print statements

#=========================================+
# The time delay between loops of main.py |
#=========================================+
LOOP_TIME_DELAY = 10

#=========================================================+
# The altitude (m, from GPS) where Wi-Fi must be disabled |
#     (according to FAA regulations) (not implemented)    |
#=========================================================+
CUTOFF_ALTITUDE = 1524

#=====================================================+
# The serial port device being used by UBLOX GPS UART |
#=====================================================+
GPS_DEVICE = "ttyS0"

#=====================================================+
# The maximum number of times to retry a GPS read if  |
#    unsuccessful                                     |
#=====================================================+
GPS_MAX_ATTEMPTS = 2

#====================================================+
# The maximum amount of time for a GPS read to occur |
#    (the read is retried 'GPS_MAX_ATTEMPTS' times   |
#        before giving up)                           |
#====================================================+
GPS_TIMEOUT = 2

# Finish comment desc.
RESOLUTION = "1920x1080"
SKIPPED_FRAMES = 10
CAPTURE_DELAY = 2
CAPTURED_FRAMES = 2
# Should this be moved to webcam.py?
SAVE_DIRECTORY = "../data/images"
WEBCAM_DEVICES = ["video0", "video2", "video4"]

CALLSIGN = "KE8ZXE"
SSID = "11"
BAUD_RATE = 1200
SAMPLE_RATE = 48000
