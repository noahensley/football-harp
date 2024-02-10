import wifi
import time
import board
import subprocess
import adafruit_bmp280

TIME_DELAY = 2 # in seconds
# RELATIVE_PRESSURE_AT_SEA_LEVEL = 1040 # in hPa
CUTOFF_ALTITUDE = 1524 # in meters
        
def read_sensor():
    bmp280_output = ""
    try:
        i2c = board.I2C()

        bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # change this to match the location's pressure (hPa) at sea level
    #
    # bmp280.sea_level_pressure = RELATIVE_PRESSURE_AT_SEA_LEVEL # Ironton, OH
    #
    # When the above lines are commented out, altitude readings seem more accurate?
    
    try:
        wifi.disable_wifi() if bmp280.altitude >= CUTOFF_ALTITUDE else wifi.enable_wifi()
        
        bmp280_output = f"{bmp280.temperature:0.1f},{(bmp280.pressure / 1000):0.2f},{bmp280.altitude:0.0f},"
    except Exception as e:
        print(f"An error occured: {e}")
    
    return bmp280_output
    

