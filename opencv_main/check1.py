#!/usr/bin/python3

import cv2
from picamera2 import Picamera2
from gpiozero import Servo, OutputDevice
import pygame
import time
import VL53L0X

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((100, 100))

# Define the GPIO pins
servo_pin = 18       # GPIO pin for the servo
relay1_pin = 22      # GPIO pin for relay 1 IN1
relay2_pin = 23      # GPIO pin for relay 2 IN2

# Setup the servo
servo = Servo(servo_pin, min_pulse_width=0.0010, max_pulse_width=0.0025)

# Define the initial servo positions
servo_mid = 0
servo_left = 1     # Extreme left
servo_right = -1   # Extreme right

# Setup the relay devices
relay1 = OutputDevice(relay1_pin, active_high=False)
relay2 = OutputDevice(relay2_pin, active_high=False)

# Initialize Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))

def set_servo_position(position):
    """Set the servo to a specific position (-1 to 1)."""
    if position < -1:
        position = -1
    elif position > 1:
        position = 1
    servo.value = position
    print(f"Setting servo to {position}")

def move_sequence():
    """Execute a sequence of movements with delays."""
    # 1. Move left & forward
    print("Moving servo left and relay 1 ON")
    set_servo_position(servo_left)
    relay1.on()
    time.sleep(5)
    relay1.off()

    # 2. Move right & backward
    print("Moving servo right and relay 2 ON")
    set_servo_position(servo_right)
    relay2.on()
    time.sleep(12)
    relay2.off()

    # 3. Move left & backward
    print("Moving servo left and relay 2 ON")
    set_servo_position(servo_left)
    relay2.on()
    time.sleep(12)
    relay2.off()

    # 4. Move right & forward
    print("Moving servo right and relay 1 ON")
    set_servo_position(servo_right)
    relay1.on()
    time.sleep(4)
    relay1.off()

    # 5. Move backward
    print("Centering servo and turning relay 2 ON")
    set_servo_position(servo_mid)
    relay2.on()
    time.sleep(4)
    relay2.off()

def detect_objects():
    """Function to capture an image and detect objects using the trained Haar Cascade."""
    object_detector = cv2.CascadeClassifier("/home/keshavek/Downloads/cars.xml")
    picam2.start()

    while True:
        # Capture image
        im = picam2.capture_array()

        # Convert to grayscale
        grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        # Detect objects
        objects = object_detector.detectMultiScale(grey, 1.1, 5)

        # Draw rectangles around detected objects
        for (x, y, w, h) in objects:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display image
        cv2.imshow("Camera", im)

        # If an object is detected, prompt the user
        if len(objects) > 0:
            print("Object detected!")
            action = input("Type 'c' to continue or 'q' to quit: ")
            if action == 'c':
                picam2.stop()
                cv2.destroyAllWindows()
                return True
            elif action == 'q':
                picam2.stop()
                cv2.destroyAllWindows()
                return False

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    picam2.stop()
    cv2.destroyAllWindows()
    return False

# Create VL53L0X objects for devices on each TCA9548A bus
sensors = []
for bus in range(6):
    sensor = VL53L0X.VL53L0X(TCA9548A_Num=bus + 1, TCA9548A_Addr=0x70)
    sensors.append(sensor)

# Start ranging on each TCA9548A bus
for sensor in sensors:
    sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

# Get timing
timing = sensors[0].get_timing()
if timing < 20000:
    timing = 20000
print("Timing %d ms" % (timing / 1000))

def sensor_values_within_tolerance(sensor_values, expected_values, tolerance=100):
    """Check if all sensor values are within the specified tolerance."""
    return all(abs(sensor_value - expected_value) <= tolerance
               for sensor_value, expected_value in zip(sensor_values, expected_values))

def calculate_distance_between_objects():
    """Calculate the distance between objects based on sensor readings."""
    initial_distance = sensors[2].get_distance()  # Get initial distance from the third sensor

    if initial_distance < 200:  # Initial object detected
        print("Initial object detected, starting to move backward...")
        relay2.on()  # Start moving backward
        start_time = time.time()

        while True:
            current_distance = sensors[2].get_distance()

            if current_distance > 3000:  # Object moved away (distance increased significantly)
                print("Object moved away, measuring time duration...")
                break

        # Wait until the object is detected again
        while True:
            current_distance = sensors[2].get_distance()

            if current_distance < 200:  # Object reappeared
                print("Second object detected!")
                end_time = time.time()
                relay2.off()  # Stop moving backward
                break

        duration = end_time - start_time  # Calculate the time duration for which the distance was long
        distance_between_objects = duration * 0.0497  # Calculate the distance based on time and speed

        print(f"Distance between objects: {distance_between_objects:.2f} meters")
        return distance_between_objects

try:
    distance_measurement_active = False  # Flag to control when distance measurement is active

    while True:
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print("Turning servo left")
                    set_servo_position(servo_left)  # Turn servo left
                elif event.key == pygame.K_RIGHT:
                    print("Turning servo right")
                    set_servo_position(servo_right)  # Turn servo right
                elif event.key == pygame.K_SPACE:
                    print("Centering servo")
                    set_servo_position(servo_mid)  # Center the servo

                elif event.key == pygame.K_UP:
                    print("Turning relay 1 ON")
                    relay1.on()  # Turn on relay 1

                elif event.key == pygame.K_DOWN:
                    print("Down Arrow pressed, turning relay 2 ON")
                    relay2.on()  # Turn on relay 2

                elif event.key == pygame.K_RETURN:  # Enter key pressed
                    print("Enter key pressed, starting object detection...")
                    if detect_objects():  # Start object detection
                        print("Checking sensor values...")
                        sensor_values = []
                        for i, sensor in enumerate(sensors[:5]):  # Only check the first 5 sensors
                            distance = sensor.get_distance()
                            sensor_values.append(distance)

                        expected_values = [8100, 8100, 190, 430, 8100]
                        if sensor_values_within_tolerance(sensor_values, expected_values):
                            print("Sensor values within tolerance, calculating distance between objects...")
                            distance = calculate_distance_between_objects()  # Calculate distance between objects
                            if distance > 1.05:
                                print("Distance greater than 1.05 meters, executing move sequence.")
                                move_sequence()  # Execute movement sequence
                            else:
                                print("Distance less than or equal to 1.05 meters, sequence not executed.")
                        else:
                            print("Sensor values not within tolerance, sequence not executed.")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    print("Centering servo")
                    set_servo_position(servo_mid)  # Center the servo when key is released
                elif event.key == pygame.K_UP:
                    print("Turning relay 1 OFF")
                    relay1.off()  # Turn off relay 1
                elif event.key == pygame.K_DOWN:
                    print("Turning relay 2 OFF")
                    relay2.off()  # Turn off relay 2

        time.sleep(timing / 1000000.00)

except KeyboardInterrupt:
    print("Program terminated")

finally:
    for sensor in sensors:
        sensor.stop_ranging()

    print("All sensors stopped")
    servo.value = servo
