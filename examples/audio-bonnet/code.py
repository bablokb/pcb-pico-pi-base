# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
CircuitPython I2S MP3 playback example.
Plays a single MP3 once.

See: https://learn.adafruit.com/circuitpython-essentials/circuitpython-mp3-audio
     https://learn.adafruit.com/mp3-playback-rp2040/pico-i2s-mp3
"""
import board
import audiomp3
import audiobusio

# The speaker-bonnet uses pins GPIO18, GPIO19 and GPIO21
# see https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/pinouts

audio = audiobusio.I2SOut(board.GPIO18, board.GPIO19, board.GPIO21)

mp3 = audiomp3.MP3Decoder(open("slow.mp3", "rb"))

audio.play(mp3)
while audio.playing:
    pass

print("Done playing!")
