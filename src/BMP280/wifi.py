import subprocess
import time

def enable_wifi():
    subprocess.run(['sudo', 'ifconfig', 'wlan0', 'up'])
    print("Wi-Fi enabled")

def disable_wifi():
    subprocess.run(['sudo', 'ifconfig', 'wlan0', 'down'])
    print("Wi-Fi disabled")
