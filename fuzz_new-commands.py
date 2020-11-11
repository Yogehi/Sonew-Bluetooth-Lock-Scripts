'''
Attempts to brute force the lock for new commands.

All commands used in this lock look like this:

0xXX 0xYY 0xZZ

0xXX = HEX between 0 and 255
0xYY = HEX, this can be repeated up to 18 times
0xZZ = HEX between 0 and 255

So a valid command can look like:

0xXX 0xYY 0xZZ

or

0xXX 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xYY 0xZZ

or anything in between.

The key is that the BLE message starts and ends with specific values, as well as be a specific length. If those values and the length is valid, then the lock will respond with *something*. If those values are not valid, then the lock won't respond at all.

For example, the "open lock" command is:

0xFE 0x4F 0x50 0x45 0x4E 0x00 0x00 0x00 0x00 0xFD

The lock will always respond as long as the above message:

* starts with 0xFE
* is 10 bytes in total length
* ends with 0xFD

So the lock will still respond with *something* if we were to send:

0xFE 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0xFD

If we were to send either of the following, which has invalid start/end values or an incorrect length, then the lock will not respond:

0xFF 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0xFD
0xFE 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0xFD
0x99 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00

This script will atempt to brute force hidden commands not found in the Android app. Admitingly I couldn't dump the firmware from the lock, so this was the next best solution.

This script took me about 2 months to complete, brute forcing against two different locks at the same time using different start/end values. I went through at least 8 batteries. And this method is unstable because the lock itself will randomly disconnect. 

To use this script:

* set payload1 to whatever decimal value you want the first byte of the payload to be
* set payload2 to whatever decimal value you want the last byte of the payload to be

Try to keep track of what values you ended up sending. I've included "hidden commands" I found through this process already at the bottom of this script.
'''
import pygatt
from binascii import hexlify
import sys
import math
from concurrent import futures
import random
import time

adapter = pygatt.backends.GATTToolBackend('hci0')

def handle_data(handle, value):
    response = hexlify(value)
    print("Received repsonse (%s)" % str(response))

def decimal_to_hexadecimal(dec): 
    decimal = int(dec) 
    return hex(decimal)

def fuzz_function(payload1, payload2, paddingCounter):
	#create temp code
	temp_code_length = paddingCounter + 2
	temp_code_array = bytearray(temp_code_length)
	#create byte array payload
	temp_code_array[0] = payload1
	temp_code_array[temp_code_length - 1] = payload2
	#temp_code_array[temp_code_length]
	print("Payload1: %s, PaddingCounter: %s, Payload2: %s" % (payload1, paddingCounter, payload2))
	device.char_write("0000ffd9-0000-1000-8000-00805f9b34fb", temp_code_array)

adapter.start()
device = adapter.connect('28:EC:9A:09:C7:2B')

device.subscribe("0000ffd4-0000-1000-8000-00805f9b34fb",callback=handle_data, wait_for_response=False)
device.subscribe("0000ffdf-0000-1000-8000-00805f9b34fb", indication=False, wait_for_response=True)

payload1 = 0
paddingCounter = 1

# modify payload 2
payload2 = 0

while payload2 != 256:
	while paddingCounter != 19:
		fuzz_function(payload1, payload2, paddingCounter)
		paddingCounter = paddingCounter + 1
	paddingCounter = 1
	payload2 = payload2 + 1

adapter.stop()

# confirmed to have commands, but they're all part of already established transmission codes
# 40 = 28
# 41 = 29
# 253 = fd
# 254 = fe
# 255 = ff

# confirmed hidden command
# [28:EC:9A:06:47:9E][LE]> char-write-cmd 0x004d ff010203040102010203040304fe #change physical code to up, down, left, right, left right
# Notification handle = 0x0038 value: 60 f0 00 95 # success
# [28:EC:9A:06:47:9E][LE]> char-write-cmd 0x004d c90102030401029c # send physcial code up, down, left, right, up, down
# Notification handle = 0x0038 value: e0 0f 00 0e # failed
# [28:EC:9A:06:47:9E][LE]> char-write-cmd 0x004d c90102030403049c # send physical code up, down, left, right, left, right
# Notification handle = 0x0038 value: e0 f0 00 0e # success

# concifmed hidden command
# [28:EC:9A:09:EC:EF][LE]> char-write-cmd 0x004d ca00000000000000000000000000000000cb
# Notification handle = 0x0038 value: f9 ae dd 04 4b 64 1a 9d 2a 3f 09 86 35 3d c6 3c 60 f8 
# [28:EC:9A:09:EC:EF][LE]> char-write-cmd 0x004d ca00000000000000000000000000000001cb
# Notification handle = 0x0038 value: f9 26 36 17 75 27 45 24 82 1f 6b 25 1d 79 6d bc f3 f8 
# [28:EC:9A:09:EC:EF][LE]> char-write-cmd 0x004d ca00000000000000000000000000000002cb
# Notification handle = 0x0038 value: f9 8f 90 9a f0 6f f8 b2 07 53 43 86 aa db cd 5f c4 f8 
# [28:EC:9A:09:EC:EF][LE]> char-write-cmd 0x004d ca00000000000000000000000000000003cb
# Notification handle = 0x0038 value: f9 4b a9 32 7c 82 41 d8 8a 6c 5e 62 ee e9 09 70 4f f8 
# [28:EC:9A:09:EC:EF][LE]> char-write-cmd 0x004d ca00000000000000000000000000000004cb
# Notification handle = 0x0038 value: f9 a0 2f 30 b3 7e eb df 2c 3e a3 c8 59 55 c4 4d 43 f8 
# [28:EC:9A:09:EC:EF][LE]> char-write-cmd 0x004d ca00000000000000000000000000000005cb
# Notification handle = 0x0038 value: f9 cb 75 a3 cc dd 58 cf 62 a4 93 bb c5 3f 24 05 54 f8

# confirmed hidden command 
# [28:EC:9A:09:EC:EF][LE]> char-write-cmd 0x004d CB1D3A4C43110E342D274C4929322D4059CA
# Notification handle = 0x0038 value: f9 34 9c 20 e7 20 af c9 5c 15 0a df 17 52 89 93 ba f8
# [28:EC:9A:09:EC:EF][LE]> char-write-cmd 0x004d CB00000000000000000000000000000000CA
# Notification handle = 0x0038 value: f9 f6 dc e3 51 e6 78 d4 fa 5e 75 38 00 dd ed 93 3c f8 

# confirmed hidden command
# [28:EC:9A:09:EC:EF][LE]> char-write-cmd 0x004d fd00000000fc
# Notification handle = 0x0038 value: 90 0f 00 09 
