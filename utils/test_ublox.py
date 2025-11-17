import serial
import time
from datetime import datetime

baud_rates = [9600]

def read_serial():
    for baud in baud_rates:
        print(f"Trying baud {baud}...")
        ser = serial.Serial("/dev/ttyAMA0", baudrate=baud, timeout=1)
        print("Reading raw GPS data...")
        with open("ublox_log.txt", "a") as fp:
            for i in range(5):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                line = ser.readline()
                line = f"[{timestamp]} {line}\n"
                print(line, file=fp)
                time.sleep(0.5)

