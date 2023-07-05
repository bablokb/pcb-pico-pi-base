# ----------------------------------------------------------------------------
# Example program for the i2c-multiplexer-pHat from 8086net
# (e.g. from Pimoroni, The PiHut, Tindie)
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/pcb-pico-pi-base
#
# ----------------------------------------------------------------------------

import time
import board
import busio
import adafruit_tca9548a
import adafruit_ahtx0

#PIN_SCL = board.GP27
#PIN_SDA = board.GP26
PIN_SCL  = board.SCL
PIN_SDA  = board.SDA

i2c = busio.I2C(sda=PIN_SDA,scl=PIN_SCL)

tca = adafruit_tca9548a.TCA9548A(i2c)

sensors = []
sensors.append(adafruit_ahtx0.AHTx0(tca[0]))
sensors.append(adafruit_ahtx0.AHTx0(tca[1]))

while True:
  for i in range(len(sensors)):
    t = sensors[i].temperature
    h = sensors[i].relative_humidity
    print(f"sensor[{i}]: T: {t:0.1f}°C, H: {h:0.0f}%")  
  time.sleep(5)
