import subprocess

def is_wifi_enabled():
    """
    Checks if the Wi-Fi interface (wlan0) is enabled.
    
    Returns:
        bool: True if Wi-Fi is enabled, False otherwise.
    """
    try:
        result = subprocess.run(['sudo', 'ifconfig', 'wlan0'], capture_output=True, text=True, check=True)
        return 'UP' in result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error checking Wi-Fi status: {e}")
        return False

def enable_wifi():
    """
    Enables the Wi-Fi interface (wlan0) if it is not already enabled.
    """
    try:
        if not is_wifi_enabled():
            subprocess.run(['sudo', 'ifconfig', 'wlan0', 'up'], check=True)
            print("Wi-Fi enabled")
        else:
            print("Wi-Fi already enabled")
    except subprocess.CalledProcessError as e:
        print(f"Error enabling Wi-Fi: {e}")

def disable_wifi():
    """
    Disables the Wi-Fi interface (wlan0) if it is enabled.
    """
    try:
        if is_wifi_enabled():
            subprocess.run(['sudo', 'ifconfig', 'wlan0', 'down'], check=True)
            print("Wi-Fi disabled")
        else:
            print("Wi-Fi already disabled")
    except subprocess.CalledProcessError as e:
        print(f"Error disabling Wi-Fi: {e}")
