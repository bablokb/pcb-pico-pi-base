# -------------------------------------------------------------------------
# CircuitPython driver for Pimoroni's wHat e-ink display.
#
# This has only been tested for the black&white variant, but should also
# work for the color-versions of this display.
#
# Author: Bernhard Bablok
# License: MIT
#
# This is a port of the what-driver from: https://github.com/pimoroni/inky
# The original MIT-License is Copyright (c) 2018 Pimoroni Ltd.
#
# Website: https://github.com/bablokb/circuitpython-examples
#
# -------------------------------------------------------------------------

import displayio

_LUTS = {
  'black': [
    0b01001000, 0b10100000, 0b00010000, 0b00010000, 0b00010011, 0b00000000, 0b00000000,
    0b01001000, 0b10100000, 0b10000000, 0b00000000, 0b00000011, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b01001000, 0b10100101, 0b00000000, 0b10111011, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0x10, 0x04, 0x04, 0x04, 0x04,
    0x10, 0x04, 0x04, 0x04, 0x04,
    0x04, 0x08, 0x08, 0x10, 0x10,
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00,
    ],
  'red': [
    0b01001000, 0b10100000, 0b00010000, 0b00010000, 0b00010011, 0b00000000, 0b00000000,
    0b01001000, 0b10100000, 0b10000000, 0b00000000, 0b00000011, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b01001000, 0b10100101, 0b00000000, 0b10111011, 0b00000000, 0b00000000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0x40, 0x0C, 0x20, 0x0C, 0x06,
    0x10, 0x08, 0x04, 0x04, 0x06,
    0x04, 0x08, 0x08, 0x10, 0x10,
    0x02, 0x02, 0x02, 0x40, 0x20,
    0x02, 0x02, 0x02, 0x02, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00
    ],
  'red_ht': [
    0b01001000, 0b10100000, 0b00010000, 0b00010000, 0b00010011, 0b00010000, 0b00010000,
    0b01001000, 0b10100000, 0b10000000, 0b00000000, 0b00000011, 0b10000000, 0b10000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b01001000, 0b10100101, 0b00000000, 0b10111011, 0b00000000, 0b01001000, 0b00000000,
    0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0x43, 0x0A, 0x1F, 0x0A, 0x04,
    0x10, 0x08, 0x04, 0x04, 0x06,
    0x04, 0x08, 0x08, 0x10, 0x0B,
    0x02, 0x04, 0x04, 0x40, 0x10,
    0x06, 0x06, 0x06, 0x02, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00
    ],
  'yellow': [
    0b11111010, 0b10010100, 0b10001100, 0b11000000, 0b11010000, 0b00000000, 0b00000000,
    0b11111010, 0b10010100, 0b00101100, 0b10000000, 0b11100000, 0b00000000, 0b00000000,
    0b11111010, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,
    0b11111010, 0b10010100, 0b11111000, 0b10000000, 0b01010000, 0b00000000, 0b11001100,
    0b10111111, 0b01011000, 0b11111100, 0b10000000, 0b11010000, 0b00000000, 0b00010001,
    0x40, 0x10, 0x40, 0x10, 0x08,
    0x08, 0x10, 0x04, 0x04, 0x10,
    0x08, 0x08, 0x03, 0x08, 0x20,
    0x08, 0x04, 0x00, 0x00, 0x10,
    0x10, 0x08, 0x08, 0x00, 0x20,
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00,
    ]
  }

_INIT_SEQUENCE = (
  b"\x74\x01\x54"  # Set Analog Block Control
  b"\x7e\x01\x3b"  # Set Digital Block Control
  b"\x01\x03\x2c\01\x00"  # Gate setting 2c01: height 300= 0x012C
  b"\x03\x01\x17"  # Gate Driving Voltage
  b"\x04\x03\x41\xAC\x32"  # Source Driving Voltage
  b"\x3a\x01\x07"  # Dummy line period
  b"\x3b\x01\x04"  # Gate line width
  b"\x11\x01\x03"  # Data entry mode setting 0x03 = X/Y increment
  b"\x2c\x01\x3c"  # VCOM Register, 0x3c = -1.5v?
  b"\x3c\x01\x00"
)

_REFRESH_SEQUENCE = (
  b"\x22\x01\xC7"     # Display Update Sequence
  b"\x20"             # Trigger Display Update
)

_STOP_SEQUENCE = (
  b"\x10\x01"         # Enter Deep Sleep
)

class Inky_wHat(displayio.EPaperDisplay):
  r"""Inky_wHat driver

  :param bus: The data bus the display is on
  :param \**kwargs:
    See below

    :Keyword Arguments:
      * *width* (``int``) --
      Display width
      * *height* (``int``) --
      Display height
      * *rotation* (``int``) --
          Display rotation
  """

  def __init__(self, bus: displayio.FourWire,
               color='black', border_color='black',
               black_bits_inverted=False,
               **kwargs) -> None:

    if color not in ('red', 'black', 'yellow'):
      raise ValueError(f"color {color} is not supported!")
    if border_color not in ('red', 'black', 'yellow', 'white'):
      raise ValueError(f"border-color {border_color} is not supported!")

    if border_color == 'black':
      init_sequence = _INIT_SEQUENCE+b"\x3c\x01\x00"
    elif border_color == 'red':
      init_sequence = _INIT_SEQUENCE+b"\x3c\x01\x73"
    elif border_color == 'yellow':
      init_sequence = _INIT_SEQUENCE+b"\x3c\x01\x33"
    elif border_color == 'white':
      init_sequence = _INIT_SEQUENCE+b"\x3c\x01\x31"

    # Set voltage of VSH and VSL
    if color == 'yellow':
      init_sequence = init_sequence+b"\x04\x03\x07\xAC\x32"
    elif color == 'red':
      init_sequence = init_sequence+b"\x04\x03\x30\xAC\x22"

    # Set LUTs
    ll = len(_LUTS[color])
    init_sequence = init_sequence+b"\x32"+bytes([ll])+bytes(_LUTS[color])

    # Set RAM X Start/End: 400//8-1 = 49 = 0x31
    init_sequence = init_sequence+b"\x44\x02\x00\x31"
    # Set RAM Y Start/End: 300 = \x01\x2c -> \x2c\x01
    init_sequence = init_sequence+b"\x45\x04\x00\00\x2c\x01"

    super().__init__(
      bus,
      init_sequence,
      _STOP_SEQUENCE,
      **kwargs,
      width=400,
      height=300,
      ram_width=400,
      ram_height=300,
      busy_state=True,
      write_black_ram_command=0x24,
      write_color_ram_command=0x26,
      refresh_display_command=_REFRESH_SEQUENCE,
      seconds_per_frame=2,
      black_bits_inverted=black_bits_inverted,
      refresh_time=2.0,
    )
