import gpsd
import wifi
import time

WAIT = 10
FT2M = 12 * 2.54 / 100 ## feet to meters
WIFIALT = 5000 * FT2M 

print("Target Alt", WIFIALT, 'm')

gpsd.connect()

while True:
    try:
        packet = gpsd.get_current()
        print(packet)
        if packet.mode >= 3:
            print("alt: ", packet.altitude())
            if packet.altitude() > WIFIALT:
                wifi.disable_wifi() 
            else:
                wifi.enable_wifi()            
    except:
        print("Error - Retry")

    time.sleep(WAIT)


