#!/usr/bin/python3

import cv2
from picamera2 import Picamera2
from gpiozero import Servo, OutputDevice
import pygame
import time

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
relay1 = OutputDevice(relay1_pin, active_high=False)  # Active high means relay is on when GPIO is high
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
    relay1.on()  # Forward
    time.sleep(5)  # Wait for 5 seconds
    relay1.off()  # Turn off relay 1

    # 2. Move right & backward
    print("Moving servo right and relay 2 ON")
    set_servo_position(servo_right)
    relay2.on()  # Backward
    time.sleep(12)  # Wait for 12 seconds
    relay2.off()  # Turn off relay 2

    # 3. Move left & backward
    print("Moving servo left and relay 2 ON")
    set_servo_position(servo_left)
    relay2.on()  # Backward
    time.sleep(12)  # Wait for 12 seconds
    relay2.off()  # Turn off relay 2

    # 4. Move right & forward
    print("Moving servo right and relay 1 ON")
    set_servo_position(servo_right)
    relay1.on()  # Forward
    time.sleep(4)  # Wait for 4 seconds
    relay1.off()  # Turn off relay 1

    # 5. Move backward
    print("Centering servo and turning relay 2 ON")
    set_servo_position(servo_mid)
    relay2.on()  # Backward
    time.sleep(4)  # Wait for 4 seconds
    relay2.off()  # Turn off relay 2

def detect_objects():
    """Function to capture an image and detect objects using the trained Haar Cascade."""
    object_detector = cv2.CascadeClassifier("/path/to/your/haar/cascade.xml")
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

try:
    while True:
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
                    print("Turning relay 2 ON")
                    if detect_objects():  # Check for object detection
                        move_sequence()  # Execute movement sequence
                    relay2.on()  # Turn on relay 2

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

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program terminated")

finally:
    # Cleanup
    servo.value = servo_mid
    relay1.off()
    relay2.off()
    pygame.quit()
