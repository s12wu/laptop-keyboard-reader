#circuitpython port of Matrix_Decoder_LC.ino for Raspberry pi pico

# finding keyboard matrix pinout

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

import board
import digitalio
from busio import I2C
import time
import microcontroller

# Function to set a pin as an input (external pullup is soldered to the board) so it's high unless grounded by a key press
def go_z(p):
    pins[p].direction = digitalio.Direction.INPUT #set as input
    pins[p].pull = None


# Function to set a pin as an output and drive it to a logic low (0 volts)
def go_0(p):
    pins[p].pull = None                            #disable pullup
    pins[p].direction = digitalio.Direction.OUTPUT #set as output
    pins[p].value = 0                              #drive low



kbd = Keyboard(usb_hid.devices)

from adafruit_mcp230xx.mcp23017 import MCP23017
i2c = I2C(board.GP27, board.GP26, frequency=1000000)
mcp = MCP23017(i2c)

KBD_pinnumbers = [board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10,
                  board.GP11, board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17, board.GP18, board.GP19, board.GP20,
                  board.GP21,
                  mcp.get_pin(0),mcp.get_pin(1),mcp.get_pin(2)]

pin_count = len(KBD_pinnumbers)

pins = []
for x,p in enumerate(KBD_pinnumbers):
    if x<20: pins.append(digitalio.DigitalInOut(p))
    else: pins.append(p)

#set each pin as input
for p in range(pin_count):
    go_z(p)

print ("Hello world! Press a key and it's combination will be printed out.")

while True:

    for i in range(pin_count-1):
        go_0(i) #set this Pin low
        #check which pin it is connected to (if any)
        for j in range(i+1, pin_count):
            go_z(j)
            if pins[j].value == 0: #is there a connection?
                print(i,j,"-",KBD_pinnumbers[i],KBD_pinnumbers[j])
                x = 0
                while pins[j].value == 0:
                    #will hang here if pins are shortened
                    x+=1

        go_z(i) #release pin

