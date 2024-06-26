pcb-pico-pi-base
================

This projects provides two adapter-boards to run Pi-hats with a Pico.

The "pico-zero-base":

![](pico-zero-base.jpg)

and the "pico-pi-base":

![](pico-pi-base.jpg)

The boards support (besides digital IO) I2C, I2S and SPI.


Supported Hats
--------------

The following hats were successfully tested:

  - Scroll pHat HD
  - Touch pHat
  - 4-Letter pHat
  - LED-Shim
  - Button-Shim
  - Pirate-Audio Speaker-Hat
  - Pirate-Audio Shim
  - Adafruit Speaker Bonnet
  - Display-Otron-Hat
  - InkyImpression  5.7"
  - Inky wHAT (black and white version)
  - Waveshare 4 inch RPi LCD (A)
  - I2C-Multiplexer-pHat

See the [examples page](examples/Readme.md) for details.


Hardware
--------

KiCad design-files are in `pico-zero-base.kicad` and in `pico-pi-base.kicad`
respectively. Ready to upload production files for JLCPCB are in `production_files`.

Except for I2C-pullups (and VSYS-diode on pico-pi-base) the adapter-boards
only map the pins of the Pico to pins of the Pi. The current versions
support I2C, SPI0, SPI1, I2S.

Schematic, layout and 3D-rendered images for pico-zero-base:

![](schematic-zero-base.png)
![](pcb-layout-zero-base.png)
![](pcb-3D-top-zero-base.png)
![](pcb-3D-bot-zero-base.png)

Schematic, layout and 3D-rendered images for pico-pi-base:

![](schematic-pi-base.png)
![](pcb-layout-pi-base.png)
![](pcb-3D-top-pi-base.png)
![](pcb-3D-bot-pi-base.png)


Software
--------

Since you cannot run Linux-software on the Pico, you need to check if there is a
Pico-driver available for your hats or adapt existing Pi drivers to the Pico. Since
many hats have python-drivers, this is not too difficult. Most hats only use
I2C and/or SPI anyhow.

In the directory `lib` you will find CircuitPython drivers for the supported
hats, unless there is a ready to use driver available.

The directory `examples` contains example programs.

The software currently assumes that you use special CircuitPython-builds
that do the pin mapping (see the directory `circuitpython`).
If not, you have to manually look up the [mapping](mapping.ods).

Porting to MicroPython from CircuitPython should be very simple, since
CircuitPython is only a fork of MicroPython and all the drivers use only
I2C, SPI and digital-IO.


License
-------

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International
License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]:
https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
