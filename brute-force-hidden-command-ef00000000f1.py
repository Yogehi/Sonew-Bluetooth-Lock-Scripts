'''
One of the hidden commands I found. This script is used to try to figure out what this command does. I also never got anywhere with this.
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

def fuzz_function(payload1, payload2, payload3, payload4, payload5, payload6):
	#create temp code
	temp_code_length = 6
	temp_code_array = bytearray(temp_code_length)
	#create byte array payload
	temp_code_array[0] = payload1
	temp_code_array[1] = payload2
	temp_code_array[2] = payload3
	temp_code_array[3] = payload4
	temp_code_array[4] = payload5
	temp_code_array[5] = payload6
	#temp_code_array[temp_code_length]
	print("payload2 = %s, payload3 = %s, payload4 = %s, payload5 = %s" % (payload2, payload3, payload4, payload5))
	device.char_write("0000ffd9-0000-1000-8000-00805f9b34fb", temp_code_array)

adapter.start()
device = adapter.connect('28:EC:9A:09:C7:2B')

device.subscribe("0000ffd4-0000-1000-8000-00805f9b34fb",callback=handle_data, wait_for_response=False)
device.subscribe("0000ffdf-0000-1000-8000-00805f9b34fb", indication=False, wait_for_response=True)


payload1 = 239
payload2 = 0
payload3 = 35
payload4 = 119
payload5 = 226
payload6 = 241

while payload2 != 256:
	while payload3 != 256:
		while payload4 != 256:
			while payload5 != 256:
				fuzz_function(payload1, payload2, payload3, payload4, payload5, payload6)
				payload5 = payload5 + 1
			payload5 = 0
			payload4 = payload4 + 1
		payload5 = 0
		payload4 = 0
		payload3 = payload3 + 1
	payload5 = 0
	payload4 = 0
	payload3 = 0
	payload2 = payload2 + 1

adapter.stop()

# if payload3 = 10, get the response "90f00009"
#	payload4 and payload5 can be whatever
#	what matters is that payload3 has to equal 10, 11, 12, 13, 14, 15, 16, 17, 18, 19
