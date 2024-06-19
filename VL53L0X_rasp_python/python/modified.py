#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2017 John Bryan Moore
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import VL53L0X
import smbus

# Initialize the I2C bus
bus = smbus.SMBus(1)

# Function to select a channel on the TCA9548A multiplexer
def select_channel(channel):
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be an integer between 0 and 7")
    bus.write_byte(0x70, 1 << channel)

# Create a VL53L0X object
tof = VL53L0X.VL53L0X()

# Define channels for each sensor
channel1 = 0  # TCA9548A bus 1
channel2 = 1  # TCA9548A bus 2

# Select and start ranging on TCA9548A bus 1
select_channel(channel1)
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

# Select and start ranging on TCA9548A bus 2
select_channel(channel2)
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

timing = tof.get_timing()
if timing < 20000:
    timing = 20000
print("Timing %d ms" % (timing / 1000))

for count in range(1, 9999):
    # Select channel 1 and get distance
    select_channel(channel1)
    distance1 = tof.get_distance()
    if distance1 > 0:
        print("1: %d mm, %d cm, %d" % (distance1, (distance1 / 10), count))

    # Select channel 2 and get distance
    select_channel(channel2)
    distance2 = tof.get_distance()
    if distance2 > 0:
        print("2: %d mm, %d cm, %d" % (distance2, (distance2 / 10), count))

    time.sleep(timing / 1000000.00)

# Stop ranging on both channels
select_channel(channel1)
tof.stop_ranging()
select_channel(channel2)
tof.stop_ranging()

