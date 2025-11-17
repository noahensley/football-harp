import serial

ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
ser.write(b"TEST\n")
received = ser.readline()
print(f"SENT: TEST\t RECEIVED: {received}")
ser.close()
