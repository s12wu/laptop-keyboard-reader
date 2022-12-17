# laptop-keyboard-reader
Most laptop keyboards (all the ones I own) have 20-26 pin ribbon cable. Here, a unique pair of the many ribbon cable contacts is connected for each key, by which the keystroke can be determined .

This circuitpyhon program for a Raspberry Pi Pico reads this keyboard format and emulates a USB HID keyboard to which all keystrokes are passed, so it can be used as a "normal" USB keyboard.

In my case, most of the ports (23 on my keyboard) are connected directly to the GPIO pins on the Pi Pico, with the remaining three going through the I²C port expander MCP23017. I do this because my Pico in my laptop also controls the screen brightness and monitors the battery status, for which I need a few more pins.

For your keyboard you have to adapt the keymap list, because the combinations are different for every keyboard model.
The contacts can be freely distributed over the pico's GPIOs and the port expander, they have to be entered in the KBD_pinnumbers list accordingly. However, the port expander is quite slow compared to the internal GPIOs, so as few connections as possible should run through it.
With my 3 connections via the expander I get a time to fetch the whole matrix (netbook keyboard with 84 keys) of about 25ms.
The typing experience has no difference to the time when the keyboard was connected directly to the netbook motherboard (larger input lag was not noticeable, I do not experience for example lost keystrokes when typing very fast).

Heavily inspired by https://www.instructables.com/How-to-Make-a-USB-Laptop-Keyboard-Controller/

## Decoding your keymap
The MatrixDecoder.py program can be used to decode your keyboard matrix.
How to use it:
1. Make a list of all the keys you have on your keyboard
2. Downlad the MatrixDecoder.py file and save it as code.py on your Pico's CIRCUIPY drive.
3. Adapt the pin numbers to match your setup
3. Watch the console when pressing each key at a time, note down the two numbers for your keys.
4. Put them into the keymap list in the main program.

Note that the decoder program has to check every possible combination and not just the ones that really correspond to a key (in my case 276 instead of 84), so it might not detect your keystroke is you're pressing very shortly, especially if you use the much slower port expander for a few of the pins.

## Localization:
You can use a layout from https://www.neradoc.me/layouts/ if you have a non-US keyboard.
Create your ZIP package and save the keycode_win_XX.py file in the CIRCUIPY/lib directory.
Then customize the code to import it.
You can look at the keycode_win_XX.py file to see the allowed keys on that language's keyboard layout.

