from gpiozero import Servo
from time import sleep

# Define the GPIO pin for the servo
servo_pin = 17  # Note: This uses BCM numbering

# Setup the servo
servo = Servo(servo_pin)

def set_angle(angle):
    # Function to set the angle of the servo
    # Convert angle (0-180) to value (-1 to 1) for gpiozero Servo
    value = (angle / 180.0) * 2 - 1
    servo.value = value
    sleep(1)

try:
    # Move the servo to specific angles
    angles = [0, 45, 90, 135, 180]
    for angle in angles:
        set_angle(angle)
        print(f"Angle: {angle}")

except KeyboardInterrupt:
    print("Stopping servo and cleaning up GPIO")

