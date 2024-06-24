# test_calculator.py

import sys
sys.path.append('../bin')  # Add the path to the shared library

import calculator

print("Addition:", calculator.add(5, 3))
print("Subtraction:", calculator.subtract(5, 3))
print("Multiplication:", calculator.multiply(5, 3))
print("Division:", calculator.divide(5, 3))

