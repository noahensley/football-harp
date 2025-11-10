import serial
from ubxtranslator import core


def read_ublox_gps(gps_port="ttyS0"):
    """
    Read from the serial port used by Raspberry Pi Zero W pins GPIO14, and GPIO15
    """
    # Open the serial port where GPS is connected (GPIO14,GPIO15)
    ser = serial.Serial(gps_port, baudrate=9600, timeout=1)

    parser = core.Parser([core.RELPOSNED_MSG])

    # Read raw bytes from the GPS module
    raw_data = ser.read(1024)

    if raw_data:
        # Parse the UBX protocol messages
        parsed = parser.receive_from(raw_data)
        for msg in parsed:
            print(msg)