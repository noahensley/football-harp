import wifi
import time
import board
import subprocess
import adafruit_bmp280
from main import CUTOFF_ALTITUDE

from debug import DEBUG_MODE
        
def read_sensor():
    """
    Connects to a BMP280 sensor via I2C bus and reads temperature, pressure, and altitude.

    Returns:
        list[str]: A list of temperature, pressure, and altitude readings.
    """
    if DEBUG_MODE:
        print("Reading BMP280...")
        
    # Output initially empty
    bmp280_output_data = {}

    try:
        # Create an I2C bus object
        i2c = board.I2C()

        # Create a bmp280 object from the I2C bus
        bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c) 

        # Disables wifi if cutoff altitude has been reached
        wifi.disable_wifi() if bmp280.altitude >= CUTOFF_ALTITUDE else wifi.enable_wifi()

        # Adds collected bmp280 data to the return list
        bmp280_output_data["Temperature"] = str(round(bmp280.temperature, 1))
        bmp280_output_data["Pressure"] = str(round(bmp280.pressure / 1000, 2))
        bmp280_output_data["Altitude"] = str(round(bmp280.altitude, 0))

    except IOError as e:
        raise IOError("Error connecting to bmp280: ", e)
        
    except Exception as e:
        raise Exception("Unexpected error occured: ", e)

    # Returns the list of data
    return bmp280_output_data
    

