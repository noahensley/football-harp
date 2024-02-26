import wifi
import time
import board
import subprocess
import adafruit_bmp280
from main import CUTOFF_ALTITUDE

# RELATIVE_PRESSURE_AT_SEA_LEVEL = 1040 # in hPa
        
def read_sensor():
    bmp280_output = ""
    
    i2c = board.I2C()

    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

    
    # change this to match the location's pressure (hPa) at sea level
    #
    # bmp280.sea_level_pressure = RELATIVE_PRESSURE_AT_SEA_LEVEL # Ironton, OH
    #
    # When the above lines are commented out, altitude readings seem more accurate?
    
    
    wifi.disable_wifi() if bmp280.altitude >= CUTOFF_ALTITUDE else wifi.enable_wifi()
        
    bmp280_output = f"{bmp280.temperature:0.1f},{(bmp280.pressure / 1000):0.2f},{bmp280.altitude:0.0f},"
    
    return bmp280_output
    

