import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)  # or GPIO.BCM
GPIO.setup(11, GPIO.OUT)  # Use a pin that you have an LED or simple output device connected to

print("Setup successful")

GPIO.cleanup()

