# Test program for the Pirate Audio hat
#
# Based on: st7789_240x240_simpletest_Pimoroni_Pico_Explorer.py
# from https://github.com/adafruit/adafruit_circuitpython_st7789
#
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.

In addition: support button-input and display the button-label
"""

import board
import busio
import time
import terminalio
import digitalio
import displayio
from adafruit_display_text import label
from adafruit_st7789 import ST7789
import audiomp3
import audiobusio

# The hat uses pins GPIO18, GPIO19 and GPIO21

audio = audiobusio.I2SOut(board.GPIO18, board.GPIO19, board.GPIO21)
mp3 = audiomp3.MP3Decoder(open("slow.mp3", "rb"))

# Release any resources currently in use for the displays
displayio.release_displays()

tft_cs = board.GPIO7      # board.CE1
tft_dc = board.GPIO9      # board.MISO -> reuse unused pin
spi_mosi = board.GPIO10   # board.MOSI
spi_clk = board.GPIO11    # board.SCLK

spi = busio.SPI(spi_clk, spi_mosi)
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(display_bus, width=240, height=240, rowstart=80, rotation=180)

# buttons

btn_a = digitalio.DigitalInOut(board.GPIO5)
btn_a.direction  = digitalio.Direction.INPUT
btn_a.pull = digitalio.Pull.UP

btn_b = digitalio.DigitalInOut(board.GPIO6)
btn_b.direction  = digitalio.Direction.INPUT
btn_b.pull = digitalio.Pull.UP

btn_x = digitalio.DigitalInOut(board.GPIO16)
btn_x.direction  = digitalio.Direction.INPUT
btn_x.pull = digitalio.Pull.UP

btn_y = digitalio.DigitalInOut(board.GPIO20)  # or GPIO24 on newer boards
btn_y.direction  = digitalio.Direction.INPUT
btn_y.pull = digitalio.Pull.UP

buttons = [(btn_a,'A'),(btn_b,'B'),(btn_x,'X'),(btn_y,'Y')]

# Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(display.width,display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(200, 200, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
splash.append(inner_sprite)

# Draw a label
text_group = displayio.Group(scale=2, x=50, y=120)
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)
time.sleep(2)

while True:
  audio.play(mp3)
  while audio.playing:
    for btn,label in buttons:
      if not btn.value:
        print(f"button {label} pressed")
        text_area.text = f"Button: {label}"
        time.sleep(0.1)
