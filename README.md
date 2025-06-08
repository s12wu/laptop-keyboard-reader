# laptop-keyboard-reader
Most older laptop keyboards have 20-26 pin ribbon cable. Here, a unique pair of the many ribbon cable contacts is connected for each key, by which the keystroke can be determined.

*Newer ones might use a different protocol (Something like USB or I²C? Just guessing), I never had a newer laptop to try it. If your keyboard has way fewer than 20-26 pins on its connector, it could work differently.*

This circuitpyhon program for a Raspberry Pi Pico reads this keyboard format and emulates a USB HID keyboard to which all keystrokes are passed, so it can be used as a "normal" USB keyboard.

In my case, most of the ports (23 on my keyboard) are connected directly to the GPIO pins on the Pi Pico, with the remaining three going through the I²C port expander MCP23017. I do this because my Pico in my laptop also controls the screen brightness and monitors the battery status, for which I need a few more pins. The RP2040 GPIO internal pullups don't seem to be "powerful" enough, so I'm using external pullup resistors.

For your keyboard you have to adapt the keymap list, because the combinations are different for every keyboard model.
The contacts can be freely distributed over the pico's GPIOs and the port expander, they have to be entered in the KBD_pinnumbers list accordingly. However, the port expander is quite slow compared to the internal GPIOs, so as few connections as possible should run through it.
With my 3 connections via the expander I get a time to fetch the whole matrix (netbook keyboard with 84 keys) of about 25ms.
The typing experience has no difference to the time when the keyboard was connected directly to the netbook motherboard (larger input lag was not noticeable, I do not experience for example lost keystrokes when typing very fast). I am no typing expert though.

This was written on an original Pi Pico with CircuitPython 7.3.3 (August 2022).
Never tested newer CircuitPython versions or a Pico 2, but everything should work. Apart from using usbhid, it's not that hardware dependent.

Heavily inspired by https://www.instructables.com/How-to-Make-a-USB-Laptop-Keyboard-Controller/

## Install CircuitPython on your Pi Pico
https://circuitpython.org/downloads

It will appear as a CIRCUIPY file system and excecute the code.py program, so save the file you need as code.py

## CircuitPython libraries
Download the [CircuitPython library bundle](https://circuitpython.org/libraries).

Copy `adafruit_hid` and `adafruit_mcp230xx` to `CIRCUIPY/lib`.

Completely set up with localization, the directory structure looks like this:
```
$ tree
CIRCUIPY
├── code.py
└── lib
   ├── adafruit_hid
   │  ├── __init__.mpy
   │  ├── consumer_control.mpy
   │  ├── consumer_control_code.mpy
   │  ├── keyboard.mpy
   │  ├── keyboard_layout_base.mpy
   │  ├── keyboard_layout_us.mpy
   │  ├── keycode.mpy
   │  └── mouse.mpy
   ├── adafruit_mcp230xx
   │  ├── __init__.mpy
   │  ├── digital_inout.mpy
   │  ├── mcp23s08.mpy
   │  ├── mcp23s17.mpy
   │  ├── mcp23sxx.mpy
   │  ├── mcp23xxx.mpy
   │  ├── mcp230xx.mpy
   │  ├── mcp23008.mpy
   │  ├── mcp23016.mpy
   │  └── mcp23017.mpy
   ├── keyboard_layout_win_gr.py
   └── keycode_win_gr.py

```


## Wiring
Connect each pin coming from the keyboard connector to one GPIO pin. Place a pullup resistor (1-10 kOhm, I used 5.6kOhm) to 3.3V on each pin. Add the pin you use to the KBD_pinnumbers list in both the MatrixDecoder.py and main code.py programs.

![schematic](https://github.com/user-attachments/assets/e783ee64-9570-4d72-865b-05d721393fb0)


When using the MCP23017 port expander, connect its SCL and SDA pins to the Pi pico (SCL = GP27, SDA = GP26, see [the pinout](https://pico.pinout.xyz) and [the code definition](https://github.com/s12wu/laptop-keyboard-reader/blob/master/code.py#L130)).

And VCC and GND to 3.3V and GND.
Add the same pullup resistors to the I²C SCL and SDA lines and the keyboard pins you connected to the port expanders for good measure.

# Software side
Take a look at [https://github.com/adafruit/Adafruit_CircuitPython_HID](https://github.com/adafruit/Adafruit_CircuitPython_HID?tab=readme-ov-file#usage-example) to learn how key codes are named.

## Decoding your keymap
The MatrixDecoder.py program can be used to decode your keyboard matrix. (Find out which pin pairs correspond to which key)
How to use it:
1. Make a list of all the keys you have on your keyboard
2. Downlad the MatrixDecoder.py file and save it as code.py on your Pico's CIRCUIPY drive.
3. Adapt the pin numbers to match your setup
3. Watch the console when pressing each key at a time, note down the two numbers for your keys.
4. Put them into the keymap list in the main program.

Note that the decoder program has to check every possible combination and not just the ones that really correspond to a key (in my case 276 instead of 84), so it might not detect your keystroke is you're pressing very shortly, especially if you use the much slower port expander for a few of the pins. When running the main program later, the polling rate won't be that bad.

## Localization:
You can use a layout from https://www.neradoc.me/layouts/ if you have a non-US keyboard.
Create your ZIP package and save the keycode_win_XX.py file in the CIRCUIPY/lib directory.
Then customize the code to import it.
You can look at the keycode_win_XX.py file to see the allowed keys on that language's keyboard layout.

In my case, I used the German key codes defined in `keycode_win_gr.py`, see the [import in line 3](https://github.com/s12wu/laptop-keyboard-reader/blob/master/code.py#L3).

Replace it with the file you downloaded for your local language, **or replace the line with**

```python
from adafruit_hid.keycode import Keycode
```

if you have a US keyboard.


## Upload the main code
With the correct pins and keymap in the main code.py file, copy it to the CIRCUIPY drive of your Pi Pico.

## My Circuit
For inspiration: this is what my hand soldered board looks like. Yup, very messy.

### Top
![top](https://user-images.githubusercontent.com/90598549/216995547-305a1cce-a606-4a5e-9c67-6b7cd3c05d6c.jpg)

### Bottom
![bottom](https://user-images.githubusercontent.com/90598549/216996026-272e6ab6-c1ef-44fe-a955-342bef531a44.jpg)

The keyboard connector is the white connector at the bottom right. My connector has the pins in two rows, I clamp it to the edge of the board and solder the pins on top and bottom. The 2mm pin spacing fits reasonably well with the 2.54mm pitch of the board, if you "bend up" every 4th to 5th pin and contact them separately. (This is what happened with a pin in the first picture, the one with the insulating tape).

![connector](https://user-images.githubusercontent.com/90598549/216996898-55ff9d19-0d26-4c04-8d20-fce19af1ebd3.jpg)

