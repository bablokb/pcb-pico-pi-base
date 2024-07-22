# -------------------------------------------------------------------------
# CircuitPython driver for Pimoroni's pHat e-ink display.
#
# This has only been tested for the black&white variant, but should also
# work for the color-versions of this display.
#
# Author: Bernhard Bablok
# License: MIT
#
# This is an adaption of the Adadruit_CircuitPython_SSD1608 driver.
# The original MIT-License is
# Copyright (c) 2019 Scott Shawcroft for Adafruit Industries
#
# Website: https://github.com/bablokb/pcb-pico-pi-base
#
# -------------------------------------------------------------------------

import displayio

_START_SEQUENCE = (
  b"\x12\x00"  # Software reset
  b"\x01\x03\xf9\x00\x00"  # driver output control
  b"\x3a\x01\x1b"  # Set dummy line period
  b"\x3b\x01\x0b"  # Set gate line width
  b"\x11\x01\x03"  # Data entry sequence
  b"\x2c\x01\x70"  # Vcom Voltage
  b"\x32\x1e\x02\x02\x01\x11\x12\x12\x22\x22\x66\x69\x69\x59\x58\x99\x99\x88\x00\x00\x00\x00\xf8"
  b"\xb4\x13\x51\x35\x51\x51\x19\x01\x00"  # LUT
  b"\x3c\x01\x00"                          # border color (black)
)

_STOP_SEQUENCE = b"\x10\x01\x01"  # Enter deep sleep


class Inky_pHat(displayio.EPaperDisplay):
  """ Inky_pHat driver """

  def __init__(self, bus: displayio.FourWire,
               color='black', border_color='black',
               **kwargs) -> None:
    start_sequence = bytearray(_START_SEQUENCE)
    if border_color == 'red':
      start_sequence[-1] = 0x06
    elif border_color == 'yellow':
      start_sequence[-1] = 0x0f
    elif border_color == 'white':
      start_sequence[-1] = 0x01

    super().__init__(
      bus,
      start_sequence,
      _STOP_SEQUENCE,
      **kwargs,
      width=250,
      height=122,
      ram_width=240,
      ram_height=320,
      colstart=12,
      set_column_window_command=0x44,
      set_row_window_command=0x45,
      set_current_column_command=0x4E,
      set_current_row_command=0x4F,
      write_black_ram_command=0x24,
      refresh_display_command=0x20,
      )
