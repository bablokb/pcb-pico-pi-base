# ----------------------------------------------------------------------------
# Simple touchphat example adapted from file
# examples/buttons.py from the source repo of the Linux driver
# (https://github.com/pimoroni/touch-phat.git)
# ----------------------------------------------------------------------------

import time
import touchphat

for pad in ['Back','A','B','C','D','Enter']:
    print(f"blinking: {pad}")
    touchphat.set_led(pad, True)
    time.sleep(1)
    touchphat.set_led(pad, False)
    time.sleep(1)

@touchphat.on_touch(['Back','A','B','C','D','Enter'])
def handle_touch(event):
    print(event.name)

print("polling for touch-events...")
while True:
  touchphat.poll()
  time.sleep(0.1)
