# -------------------------------------------------------------------------
# CircuitPython driver for Waveshare 4in Pi-display.
#
# The display uses an ILI9486-chip. Waveshare attaches SPI on one side
# to a 16-bit parallel bus on the ILI9486 with two SIPO shift-registers
# in between.
#
# This setup is incompatible with any standard software-driver. The
# driver here only works with a special hacked CircuitPython-version.
#
# Author: Bernhard Bablok
# License: MIT
#
# Website: https://github.com/bablokb/circuitpython-examples
#
# -------------------------------------------------------------------------

try:
    # used for typing only
    from typing import Any
except ImportError:
    pass

import busdisplay

# init-sequence (16-bit) for Waveshare 4in display
# source:
# https://github.com/swkim01/waveshare-dtoverlays/blob/master/waveshare35a.dts
# note: this display also needs a special hacked version of CircuitPython

_INIT_SEQUENCE_16 = (
  b"\x11\x80\x78"                     # SLPOUT + 120ms delay
  b"\x3a\x02\x00\x55"                 # PIXFMT
  b"\xc2\x02\x00\x44"                 # VDVVRHEN
  b"\xc5\x08\x00\x00\x00\x00\x00\x00\x00\x00" # VCMOFSET
  b"\xe0\x1e\x00\x0f\x00\x1f\x00\x1c\x00\x0c\x00\x0f\x00\x08\x00\x48\x00\x98\x00\x37\x00\x0a\x00\x13\x00\x04\x00\x11\x00\x0d\x00\x00"
  b"\xe1\x1e\x00\x0f\x00\x32\x00\x2e\x00\x0b\x00\x0d\x00\x05\x00\x47\x00\x75\x00\x37\x00\x06\x00\x10\x00\x03\x00\x24\x00\x20\x00\x00"
  b"\xe2\x1e\x00\x0f\x00\x32\x00\x2e\x00\x0b\x00\x0d\x00\x05\x00\x47\x00\x75\x00\x37\x00\x06\x00\x10\x00\x03\x00\x24\x00\x20\x00\x00"
  b"\x29\x00"                         # DISPLAY_ON
  b"\x21\x00"                         # INVON
  b"\x36\x02\x00"                     # MADCTL, must be last
)

_MADCTL = {
    0: (480,320,b"\xe8"),
   90: (320,480,b"\x48"),
  180: (480,320,b"\x28"),
  270: (320,480,b"\x88")
  }

class ILI9486(busdisplay.BusDisplay):
  """
  ILI9488 display driver

  :param displayio.FourWire bus: bus that the display is connected to
  """

  def __init__(self, bus: displayio.FourWire, rotation=0, **kwargs: Any):
    # fix width,height and rotation
    # instead of CP rotating the content, we delegate it to the chip
    width,height,madctl = _MADCTL[rotation]
    super().__init__(bus, _INIT_SEQUENCE_16+madctl,
                     width=width,
                     height=height,
                     rotation=0,
                     **kwargs)
