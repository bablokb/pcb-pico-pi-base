# ----------------------------------------------------------------------------
# CircuitPython version of the example provided by Pimoroni.
# (https://github.com/pimoroni/button-shim)
# ----------------------------------------------------------------------------

import time
import board
import buttonshim

print("""
Button SHIM: control-main.py

Light up the LED a different color of the rainbow with each button pressed.
""")

shim = buttonshim.ButtonShim(i2c=board.I2C())

@shim.on_press(shim.BUTTON_A)
def button_a(button, pressed):
    shim.set_pixel(0x94, 0x00, 0xd3)
    print(f"button {buttonshim.NAMES[button]}")
    
@shim.on_press(shim.BUTTON_B)
def button_b(button, pressed):
    shim.set_pixel(0x00, 0x00, 0xff)
    print(f"button {buttonshim.NAMES[button]}")
    
@shim.on_press(shim.BUTTON_C)
def button_c(button, pressed):
    shim.set_pixel(0x00, 0xff, 0x00)
    print(f"button {buttonshim.NAMES[button]}")

@shim.on_press(shim.BUTTON_D)
def button_d(button, pressed):
    shim.set_pixel(0xff, 0xff, 0x00)
    print(f"button {buttonshim.NAMES[button]}")

@shim.on_press(shim.BUTTON_E)
def button_e(button, pressed):    
    shim.set_pixel(0xff, 0x00, 0x00)
    print(f"button {buttonshim.NAMES[button]}")
    
while True:
   time.sleep(.1)
   shim.poll()
