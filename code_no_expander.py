import usb_hid
from adafruit_hid.keyboard import Keyboard
from keycode_win_gr import Keycode # import your local keymap or use from adafruit_hid.keycode import Keycode for US
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import board
import digitalio
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


# definition of matrix keymap (which pin connection belongs to which key). YOURS WILL BE DIFFERENT
keymap=[
    [ 0, 15, Keycode.PRINT_SCREEN ],
    [ 0, 14, Keycode.ONE ],
    [ 0, 10, Keycode.CAPS_LOCK ],
    [ 0, 3, Keycode.X ],
    [ 0, 12, Keycode.C ],
    [ 0, 4, Keycode.B ],
    [ 0, 13, Keycode.COMMA ],
    [ 0, 2, Keycode.ALTGR ],
    [ 0, 9, Keycode.DOWN_ARROW ],
    [ 1, 7, Keycode.W ],
    [ 1, 11, Keycode.A ],
    [ 1, 6, Keycode.S ],
    [ 1, 21, Keycode.Y ],
    [ 1, 22, 0 ], #this is the FN key - it isn't reported via USB, but handeled internally
    [ 2, 22, Keycode.LEFT_ALT ],
    [ 3, 17, Keycode.FOUR ],
    [ 3, 8, Keycode.FIVE ],
    [ 3, 6, Keycode.E ],
    [ 3, 7, Keycode.R ],
    [ 3, 21, Keycode.D ],
    [ 3, 11, Keycode.F ],
    [ 3, 22, Keycode.OEM_102 ],
    [ 4, 17, Keycode.EIGHT ],
    [ 4, 8, Keycode.NINE ],
    [ 4, 6, Keycode.Z ],
    [ 4, 7, Keycode.U ],
    [ 4, 11, Keycode.J ],
    [ 4, 21, Keycode.N ],
    [ 5, 17, Keycode.AKUT ],
    [ 5, 7, Keycode.EQUALS ],
    [ 5, 6, Keycode.ENTER ],
    [ 5, 11, Keycode.FORWARD_SLASH ],
    [ 5, 22, Keycode.APPLICATION ],
    [ 6, 15, Keycode.THREE ],
    [ 6, 10, Keycode.TAB ],
    [ 6, 14, Keycode.Q ],
    [ 6, 13, Keycode.I ],
    [ 6, 12, Keycode.H ],
    [ 6, 16, Keycode.GRAVE_ACCENT ],
    [ 6, 9, Keycode.PAGE_UP ],
    [ 7, 10, Keycode.F5 ],
    [ 7, 14, Keycode.F8 ],
    [ 7, 15, Keycode.BACKSPACE ],
    [ 7, 12, Keycode.T ],
    [ 7, 13, Keycode.O ],
    [ 7, 16, Keycode.QUOTE ],
    [ 8, 10, Keycode.ESCAPE ],
    [ 8, 15, Keycode.F10 ],
    [ 8, 14, Keycode.F11 ],
    [ 8, 9, Keycode.INSERT ],
    [ 8, 12, Keycode.SEVEN ],
    [ 8, 13, Keycode.LEFT_BRACKET ],
    [ 8, 16, Keycode.SEMICOLON ],
    [ 9, 17, Keycode.DELETE ],
    [ 9, 11, Keycode.PAGE_DOWN ],
    [ 9, 22, Keycode.LEFT_ARROW ],
    [ 9, 21, Keycode.RIGHT_ARROW ],
    [ 10, 11, Keycode.F1 ],
    [ 10, 21, Keycode.F2 ],
    [ 10, 22, Keycode.F6 ],
    [ 10, 17, Keycode.ZIRKUMFLEX ],
    [ 11, 14, Keycode.F4 ],
    [ 11, 15, Keycode.TWO ],
    [ 11, 12, Keycode.G ],
    [ 11, 13, Keycode.L ],
    [ 11, 16, Keycode.MINUS ],
    [ 11, 19, Keycode.RIGHT_SHIFT ],
    [ 12, 17, Keycode.SIX ],
    [ 12, 21, Keycode.V ],
    [ 12, 22, Keycode.SPACE ],
    [ 13, 17, Keycode.ZERO ],
    [ 13, 21, Keycode.K ],
    [ 13, 22, Keycode.M ],
    [ 14, 21, Keycode.F3 ],
    [ 14, 22, Keycode.F7 ],
    [ 14, 17, Keycode.F12 ],
    [ 15, 17, Keycode.F9 ],
    [ 15, 22, Keycode.PAUSE ],
    [ 15, 21, Keycode.UP_ARROW ],
    [ 16, 17, Keycode.P ],
    [ 16, 21, Keycode.PERIOD ],
    [ 18, 22, Keycode.LEFT_CONTROL ],
    [ 18, 21, Keycode.RIGHT_CONTROL ],
    [ 19, 21, Keycode.LEFT_SHIFT ],
    [ 20, 22, Keycode.WINDOWS ]

]
#list that saves the current state of each key, 1 = released, 0 = pressed
keystatus = [1] * len(keymap)

#try connecting to USB HID, if it fails, reset and try again after 15 seconds.
#(this is needed in my environment because USB devices aren't accepted for the first few seconds)
try:
    kbd = Keyboard(usb_hid.devices)
    cc = ConsumerControl(usb_hid.devices)
except:
    print("USB error! Restarting in 15 seconds")
    time.sleep(15)
    microcontroller.reset()

#which pins is the keyboard ribbon connector connected to?
KBD_pinnumbers = [board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10,
                  board.GP11, board.GP12, board.GP13, board.GP14, board.GP15, board.GP16, board.GP17, board.GP18, board.GP19, board.GP20,
                  board.GP21]

pins = []
for x,p in enumerate(KBD_pinnumbers):
    pins.append(digitalio.DigitalInOut(p))


#set each pin as input
for p in range(23):
    go_z(p)


while True:
    for idx, line in enumerate(keymap): #check each possible combination
        go_0(line[0])
        reading = pins[line[1]].value #pull down, read, pull up
        go_z(line[0])

        if not keystatus[idx] == reading: #key status changed, report it to USB HID keyboard
            keystatus[idx] = reading
            report = (not line[2] == 0) #FN key isn't reported via USB but handled directly on the pico

            if keystatus[13] == 0 and reading == 0: #If FN button is pressed too, handle it as FN-Combination (only on key down)
                report = False
                # customize these FN-combination responses to your liking
                if line[2] == Keycode.DOWN_ARROW: #volume down
                    cc.send(ConsumerControlCode.VOLUME_DECREMENT)
                if line[2] == Keycode.UP_ARROW: #volume up
                    cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                if line[2] == Keycode.F8: #mute / unmute
                    cc.send(ConsumerControlCode.MUTE)


            if report:
                if reading == 0: #New key pressed
                    kbd.press(line[2])
                else: #Key released
                    kbd.release(line[2])




