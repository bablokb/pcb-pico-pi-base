#-----------------------------------------------------------------------------
# Sample LoRa code for a gateway on a Pico
#
# Adapted from:
#
#   Adafruit IO LoRa Gateway
#   Learn Guide: https://learn.adafruit.com/multi-device-lora-temperature-network
#   by Brent Rubell for Adafruit Industries
#   SPDX-FileCopyrightText: 2019 Brent Rubell for Adafruit Industries
#   SPDX-License-Identifier: MIT
#
# Author: Bernhard Bablok
#
# Website: https://github.com/pcb-pico-pi-base
#-----------------------------------------------------------------------------

import time
import busio
import board
from digitalio import DigitalInOut, Direction, Pull

import busio
import displayio
from terminalio import FONT
from adafruit_display_text import label
from adafruit_displayio_ssd1306 import SSD1306

import adafruit_rfm9x

# --- constants   -------------------------------------------------------------

INTERVAL = 2
RADIO_FREQ_MHZ  = 868.0
LORA_STATION_ID = 0
HEADER_TEXT = 'Datalogger Gateway'
WAIT_TEXT   = 'listening...'
ERROR_TEXT  = 'invalid data'

# --- buttons (unused)   ------------------------------------------------------
# Button A
#btnA = DigitalInOut(board.GPIO5)
#btnA.direction = Direction.INPUT
#btnA.pull = Pull.UP

# Button B
#btnB = DigitalInOut(board.GPIO6)
#btnB.direction = Direction.INPUT
#btnB.pull = Pull.UP

# Button C
#btnC = DigitalInOut(board.GPIO12)
#btnC.direction = Direction.INPUT
#btnC.pull = Pull.UP

# --- display   --------------------------------------------------------------

displayio.release_displays()
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c,device_address=0x3c)
display = SSD1306(display_bus,width=128,height=32)

group = displayio.Group()
lbl = label.Label(FONT,text=HEADER_TEXT,color=0xFFFFFF,line_spacing=1.05,
                    anchor_point=(0,0),x=0,y=4
                    )
group.append(lbl)
display.show(group)

# --- LoRa   -----------------------------------------------------------------

CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.GPIO25)
spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.node = LORA_STATION_ID
rfm9x.ack_delay = 0.1
rfm9x.tx_power = 23

# --- update display   -------------------------------------------------------

def update_display(lines=[]):
  """ update display """

  txt = f"{HEADER_TEXT}\n{lines[0]}"
  if len(lines) > 1:
    txt = f"{txt}\n{lines[1]}: {lines[2]}"
  lbl.text = txt

# --- process data   ---------------------------------------------------------

def process_data(data):
  """ process data (e.g. send into the cloud) """
  print(f"data: {data}")

# --- main-loop   ------------------------------------------------------------

update_display([WAIT_TEXT])
while True:
  packet = None

  # check for packet rx. Default timeout is 0.5
  packet = rfm9x.receive(with_ack=True,timeout=1.0)
  if packet is None:
    continue
  snr  = rfm9x.last_snr
  rssi = rfm9x.last_rssi

  # Decode packet: assume it is csv with a timestamp as first field
  try:
    data = packet.decode()
    process_data(data)
    values = data.split(',')         # expect csv
    ts = values[0].split('T')[1]     # removes date from timestamp
    # Display packet information
    update_display([f"{ts} ({snr}/{rssi})",values[1],values[2]])
  except:
    update_display([ERROR_TEXT])
  time.sleep(INTERVAL)
