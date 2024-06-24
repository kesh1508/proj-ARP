#!/usr/bin/python3

import cv2
from picamera2 import Picamera2

# Initialize face detector
face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

# Start OpenCV window thread
cv2.startWindowThread()

# Initialize Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

try:
    while True:
        # Capture image
        im = picam2.capture_array()

        # Convert to grayscale
        grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_detector.detectMultiScale(grey, 1.1, 5)

        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display image
        cv2.imshow("Camera", im)

        # If a face is detected, prompt the user
        if len(faces) > 0:
            print("Face detected!")
            action = input("Type 'c' to continue or 'q' to quit: ")
            if action == 'q':
                break

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Release resources
    picam2.stop()
    cv2.destroyAllWindows()

