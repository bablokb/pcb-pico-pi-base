# -------------------------------------------------------------------------
# Testprogram for Pimoroni's pHat e-ink display.
#
# This program is an adaption of Adafruit's ssd1608_simpletest.py from
# https://github.com/adafruit/Adafruit_CircuitPython_SSD1608
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-examples
#
# -------------------------------------------------------------------------

# pylint: disable=no-member

import time
import board
import busio
import displayio
from phat import Inky_pHat

print("starting program")
time.sleep(5)

print("releasing displays")
displayio.release_displays()

# pinout for Pimoroni pHat (Pi-names)

SCK_PIN  = board.GPIO11
MOSI_PIN = board.GPIO10
CS_PIN   = board.CE0
RST_PIN  = board.GPIO27
DC_PIN   = board.GPIO22
BUSY_PIN = board.GPIO17

spi = busio.SPI(SCK_PIN,MOSI=MOSI_PIN)
display_bus = displayio.FourWire(
  spi, command=DC_PIN, chip_select=CS_PIN, reset=RST_PIN, baudrate=488000
)
display_bus.reset()

print("creating display")
display = Inky_pHat(
  display_bus, width=250, height=122, busy_pin=BUSY_PIN, rotation=90,
  #border_color='white'
)

print("creating root-group")
g = displayio.Group()

with open("/display-ruler.bmp", "rb") as f:
  pic = displayio.OnDiskBitmap(f)
  t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
  print("appending image")
  g.append(t)

  print("starting show()")
  #display.root_group = g
  display.show(g)
  print("starting refresh()")
  display.refresh()
  print("finished")
  time.sleep(120)
