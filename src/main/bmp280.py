import wifi
import time
import board
import subprocess
import adafruit_bmp280
from main import CUTOFF_ALTITUDE
        
def read_sensor():
    """
    Connects to a BMP280 sensor via I2C bus and reads temperature, pressure, and altitude.

    Returns:
    list[float]: temperature, pressure, and altitude readings.
    """
    # Output initially empty
    bmp280_output_data = []   

    # Create an I2C bus object
    i2c = board.I2C()

    # Create a bmp280 object from the I2C bus
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c) 

    # Disables wifi if cutoff altitude has been reached
    wifi.disable_wifi() if bmp280.altitude >= CUTOFF_ALTITUDE else wifi.enable_wifi()

    # Adds collected bmp280 data to the return list
    bmp280_output_data.append(str(round(bmp280.temperature),1))
    bmp280_output_data.append(str(round(bmp280.pressure / 1000),2))
    bmp280_output_data.append(str(round(bmp280.altitude),0))

    # Returns the list of data
    return bmp280_output_data
    

