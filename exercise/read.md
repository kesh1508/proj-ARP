# Python Calculator Extension Module

This project demonstrates how to create a Python extension module in C for a simple calculator with basic arithmetic functions. The module provides functions for addition, subtraction, multiplication, and division.

## Prerequisites

- Python development headers
- GCC compiler
- Make utility

### Installing Python Development Headers

For Debian-based systems (Ubuntu, etc.):
```sh
sudo apt-get update
sudo apt-get install python3-dev
#################################################################
.
+-- calculator.c
+-- Makefile
+-- bin
�   +-- calculator.so (generated)
+-- obj
�   +-- calculator.o (generated)
+-- README.md
+-- test_calculator.py
#################################################################
