#==================================+
# Includes status print statements |
#==================================+
DEBUG_MODE = False

#==================================+
# Logs data/saves images           |
#==================================+
LOGGING_MODE = True

#==============================================+
# The time delay between loops of main service |
#                                              |
# [USED: main.py]                              |
#==============================================+
LOOP_TIME_DELAY = 60

#=========================================================+
# The altitude (m, from BMP280) where Wi-Fi must be dis-  |
#   abled according to FAA regulations)                   |
#                                                         |
# [USED: Not yet used]                                    |
#=========================================================+
CUTOFF_ALTITUDE = 1524

#=====================================================+
# The maximum number of times to retry a GPS read if  |
#   unsuccessful                                      |
#                                                     |
# [USED: ublox.poll_gps]                              |
#=====================================================+
GPS_MAX_ATTEMPTS = 10

#====================================================+
# The maximum amount of time for a GPS read to occur |
#   (the read is retried 'GPS_MAX_ATTEMPTS' times    |
#       before giving up)                            |
#                                                    |
# [USED: ublox.poll_gps]                             |
#====================================================+
GPS_TIMEOUT = 20

#===========================================+
# The resolution for fswebcam image capture |
#                                           |
# [USED: fsbwecam]                          |
#===========================================+
RESOLUTION = "1920x1080"

#=============================================+
# The number of frames to skip when capturing |
#   an image (this reduces blurry images in-  |
#   flight)                                   |
#                                             |
# [USED: fswebcam]                            |
#=============================================+
SKIPPED_FRAMES = 10

#==============================================+
# The delay between consecutive image captures |
#                                              |
# [USED: fswebcam]                             |
#==============================================+
CAPTURE_DELAY = 2

#===============================================+
# The "pre-amble" frames before the real image  |
#   frame is captured (preamble needed to apply |
#   certain capture settings)                   |
#                                               |
# [USED: fswebcam]                              |
#===============================================+
CAPTURED_FRAMES = 2

#===============================================+
# A list of the USB hub webcam video devices    |
#   (each webcam is assigned two video devices: |
#       one for video stream data and one for   |
#           metadata                            |
#                                               |
# [USED: webcam.py]                             |
#===============================================+
WEBCAM_DEVICES = ["video0", "video2", "video4"]

#========================================+
# The callsign for outgoing APRS packets | 
#                                        |
# [USED: aprs_tx.py]                     |
#========================================+
CALLSIGN = "KE8ZXE"

#=========================================+
# The SSID of the Pi APRS application     | 
#   (-11: balloons, aircraft, spacecraft, |
#       etc.)                             |
#                                         |
# [USED: aprs_tx.py]                      |
#=========================================+
SSID = "11"
