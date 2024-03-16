import subprocess

def is_wifi_enabled():
    """Checks Raspberry Pi 0W wifi status."""
    result = subprocess.run(['sudo', 'ifconfig', 'wlan0'], capture_output=True, text=True)
    return 'UP' in result.stdout

def enable_wifi():
    """Enables Raspberry Pi 0W wifi via command line."""
    if not is_wifi_enabled():
        subprocess.run(['sudo', 'ifconfig', 'wlan0', 'up'], check=True)
        print("Wi-Fi enabled")
    else:
        print("Wi-Fi already enabled")

def disable_wifi():
    """Disables Raspberry Pi 0W wifi via command line."""
    if is_wifi_enabled():
        subprocess.run(['sudo', 'ifconfig', 'wlan0', 'down'], check=True)
        print("Wi-Fi disabled")
    else:
        print("Wi-Fi already disabled")
