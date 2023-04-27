import math
import time
import colorsys

import blinkt

FALLOFF = 1.9
SCAN_SPEED = 4

i = 0
while i<3:
  blinkt.set_all(255,0,0,0.1)
  blinkt.show()
  time.sleep(1)
  blinkt.set_all(0,255,0,0.1)
  blinkt.show()
  time.sleep(1)
  blinkt.set_all(0,0,255,0.1)
  blinkt.show()
  time.sleep(1)
  i += 1

REDS = [0, 0, 0, 0, 0, 16, 64, 255, 64, 16, 0, 0, 0, 0, 0, 0]
start_time = time.monotonic()
i = 0
while i < 32:
  # Triangle wave, a snappy ping-pong effect
  delta = (time.monotonic() - start_time) * 16
  offset = int(abs((delta % len(REDS)) - blinkt.NUM_PIXELS))

  for pix in range(blinkt.NUM_PIXELS):
    blinkt.set_pixel(pix, REDS[offset + pix], 0, 0)
  blinkt.show()
  time.sleep(0.1)
  i += 1

start_time = time.monotonic()
while True:
    delta = (time.monotonic() - start_time)

    # Offset is a sine wave derived from the time delta
    # we use this to animate both the hue and larson scan
    # so they are kept in sync with each other
    offset = (math.sin(delta * SCAN_SPEED) + 1) / 2

    # Use offset to pick the right colour from the hue wheel
    hue = int(round(offset * 360))

    # Maximum number basex on NUM_PIXELS
    max_val = blinkt.NUM_PIXELS - 1

    # Now we generate a value from 0 to max_val
    offset = int(round(offset * max_val))

    for x in range(blinkt.NUM_PIXELS):
        sat = 1.0

        val = max_val - (abs(offset - x) * FALLOFF)
        val /= float(max_val)   # Convert to 0.0 to 1.0
        val = max(val, 0.0)     # Ditch negative values

        xhue = hue              # Grab hue for this pixel
        xhue += (1 - val) * 10  # Use the val offset to give a slight colour trail variation
        xhue %= 360             # Clamp to 0-359
        xhue /= 360.0           # Convert to 0.0 to 1.0

        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(xhue, sat, val)]

        blinkt.set_pixel(x, r, g, b, val / 4)

    blinkt.show()

    time.sleep(0.001)
