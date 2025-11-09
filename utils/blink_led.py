#!/usr/bin/env python3
import time

# Function to control the ACT LED
def blink_led(times=10, duration=0.1):
    """
    Blink the onboard ACT LED
    
    Args:
        times: Number of times to blink (default: 10)
        duration: Duration of each blink in seconds (default: 0.1)
    """
    led_trigger = "/sys/class/leds/ACT/trigger"
    led_brightness = "/sys/class/leds/ACT/brightness"
    
    try:
        # Save original trigger setting
        with open(led_trigger, 'r') as f:
            original_trigger = f.read().strip()
            # Extract the active trigger (between brackets)
            if '[' in original_trigger:
                original_trigger = original_trigger.split('[')[1].split(']')[0]
        
        # Set LED to manual control
        with open(led_trigger, 'w') as f:
            f.write('none')
        
        # Blink the LED
        for _ in range(times):
            # LED on
            with open(led_brightness, 'w') as f:
                f.write('1')
            time.sleep(duration)
            
            # LED off
            with open(led_brightness, 'w') as f:
                f.write('0')
            time.sleep(duration)
        
        # Restore original trigger
        with open(led_trigger, 'w') as f:
            f.write(original_trigger)
            
    except PermissionError:
        print("Error: This script requires root privileges.")
        print("Run with: sudo python3 blink_led.py")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    blink_led()
    #print("LED blink complete!")
