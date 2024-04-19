# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""
import board
import time
import terminalio
import displayio
import fourwire
import busdisplay
import busio
from adafruit_display_text import label
from ili9486_waveshare40 import ILI9486

# Release any resources currently in use for the displays
displayio.release_displays()

# pins (Pi names)
# PIN_SPI_CLK  = board.SCLK
# PIN_SPI_MOSI = board.MOSI
# PIN_SPI_MISO = board.MISO

# PIN_LCD_DC   = board.GPIO24
# PIN_LCD_CS   = board.CE0
# PIN_LCD_RST  = board.GPIO25

# PIN_TP_CS  = board.CE1
# PIN_TP_IRQ = board.GPIO17

# pins (pico pins pico-zero-base)
# PIN_SPI_CLK  = board.GP10
# PIN_SPI_MOSI = board.GP11

# PIN_LCD_DC   = board.GP27
# PIN_LCD_CS   = board.GP9
# PIN_LCD_RST  = board.GP26

# pins (pico pins pico-pi-base)
PIN_SPI_CLK  = board.GP18
PIN_SPI_MOSI = board.GP19

PIN_LCD_DC   = board.GP11
PIN_LCD_CS   = board.GP17
PIN_LCD_RST  = board.GP9


spi = busio.SPI(clock=PIN_SPI_CLK,MOSI=PIN_SPI_MOSI)
if spi.try_lock():
  spi.configure(baudrate=20_000_000)
  spi.unlock()
display_bus = fourwire.FourWire(
  spi, command=PIN_LCD_DC, chip_select=PIN_LCD_CS, reset=PIN_LCD_RST,
)
display_bus.reset()
time.sleep(0.005)

display = ILI9486(display_bus, rotation=0)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(display.width,display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(280, 200, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap,
                                  pixel_shader=inner_palette, x=20, y=20)
splash.append(inner_sprite)

# Draw a label
text_group = displayio.Group(scale=3, x=57, y=120)
text = "Hello World!"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF)
text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_group)

print("finished!")
print("press CTRL-C")
while True:
  time.sleep(1)
