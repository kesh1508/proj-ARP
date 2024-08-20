import time
import VL53L0X

from gpiozero import Servo
from time import sleep

# Define the GPIO pin for the servo
servo_pin = 17  # Note: This uses BCM numbering

# Setup the servo
servo = Servo(servo_pin)

# Create a VL53L0X object
tof = VL53L0X.VL53L0X()

# Start ranging
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
#tof.start_ranging()

timing = tof.get_timing()
if (timing < 20000):
    timing = 20000
print ("Timing %d ms" % (timing/1000))

#for count in range(1,9999999999):
    #distance = tof.get_distance()
#    if (distance > 0):
#        print ("%d mm, %d cm, %d" % (distance, (distance/10), count))

 #   time.sleep(timing/1000000.00)

#tof.stop_ranging()


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
        sleep(1)
        for count in range(1,2):
         distance = tof.get_distance()
         print ("%d mm, %d cm, %d" % (distance, (distance/10), count))

except KeyboardInterrupt:
    print("Stopping servo and cleaning up GPIO")




