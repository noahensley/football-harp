import RPi.GPIO as GPIO
import time

OUTPUT_PIN = 40
TIME_HIGH = 4

def main():
    try:
	#print("Setting GPIO mode...")
    	GPIO.setmode(GPIO.BOARD)
    	#print(f"Setting pin {OUTPUT_PIN} as GPIO.OUT (initial == LOW)...")
    	GPIO.setup(OUTPUT_PIN, GPIO.OUT, initial=GPIO.LOW)
    	print(f"Setting pin {OUTPUT_PIN} HIGH...", end="")
    	GPIO.output(OUTPUT_PIN, GPIO.HIGH)
    	print("DONE")
    	print(f"SIGNAL IS ACTIVE (pin == {OUTPUT_PIN})")
    	time.sleep(TIME_HIGH)
    	print(f"Setting pin {OUTPUT_PIN} LOW...", end="")
    	print("DONE")
    	GPIO.output(OUTPUT_PIN, GPIO.LOW)
    	GPIO.cleanup(OUTPUT_PIN)
    except Exception as e:
    	print("Error manipulating GPIO:", e)


if __name__ == "__main__":
    main()
