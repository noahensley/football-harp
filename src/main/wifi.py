import subprocess

def is_wifi_enabled():
    result = subprocess.run(['sudo', 'ifconfig', 'wlan0'], capture_output=True, text=True)
    return 'UP' in result.stdout

def enable_wifi():
    if not is_wifi_enabled():
        subprocess.run(['sudo', 'ifconfig', 'wlan0', 'up'])
        print("Wi-Fi enabled")
    else:
        print("Wi-Fi already enabled")

def disable_wifi():
    if is_wifi_enabled():
        subprocess.run(['sudo', 'ifconfig', 'wlan0', 'down'])
        print("Wi-Fi disabled")
    else:
        print("Wi-Fi already disabled.")
