# laptop-keyboard-reader
Most laptop keyboards (all the ones I own) have 20-26 pin ribbon cable. Here, a unique pair of the many ribbon cable contacts is connected for each key, by which the keystroke can be determined .

This circuitpyhon program for a Raspberry Pi Pico reads this keyboard format and emulates a USB HID keyboard to which all keystrokes are passed, so it can be used as a normal keyboard

In my case, most of the ports (23 on my keyboard) are connected directly to the GPIO pins on the Pi Pico, with the remaining three going through the I²C port expander MCP23017. I do this because my Pico in my laptop also controls the screen brightness and monitors the battery status, for which I need a few more pins.

For your keyboard you have to adapt the keymap list, because the combinations are different for every keyboard model. A program to read them will follow soon.
The contacts can be freely distributed over the pico-GPIOs and the port expander, they have to be entered in the KBD_pinnumbers list accordingly. However, the port expander is quite slow compared to the internal GPIOs, so as few connections as possible should run through it.
With my 3 connections via the expander I get a time to fetch the whole matrix (netbook keyboard with 84 keys) of about 25ms.

By the way, this README was written on this very keyboard.
