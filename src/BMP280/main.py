# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import wifi
import time
import board
import subprocess

# import digitalio # For use with SPI
import adafruit_bmp280

TIME_DELAY = 2 # seconds
RELATIVE_PRESSURE_AT_SEA_LEVEL = 1040 # hPa
CUTOFF_ALTITUDE = 1524 # meters

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bmp280.sea_level_pressure = RELATIVE_PRESSURE_AT_SEA_LEVEL # Ironton, OH

while True:
    print("%0.1f,%0.4f,%i" % (bmp280.temperature, bmp280.pressure / 1000, bmp280.altitude))
    
    if bmp280.altitude >= CUTOFF_ALTITUDE:
        disable_wifi()
    else:
        enable_wifi()
    
    time.sleep(TIME_DELAY) # two seconds

