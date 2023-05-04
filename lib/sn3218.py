# ----------------------------------------------------------------------------
# CircuitPython version of the Linux-driver provided by Pimoroni.
# (https://github.com/pimoroni/sn3218-python)
# ----------------------------------------------------------------------------

import board
import time
import digitalio
import busio
from adafruit_bus_device.i2c_device import I2CDevice

I2C_ADDRESS = 0x54
CMD_ENABLE_OUTPUT = 0x00
CMD_SET_PWM_VALUES = 0x01
CMD_ENABLE_LEDS = 0x13
CMD_UPDATE = 0x16
CMD_RESET = 0x17

class SN3218:
  default_gamma_table = [int(pow(255, float(i - 1) / 255)) for i in range(256)]

  def __init__(self,i2c,enable_mask=0b111111111111111111):

    self._i2c_device = I2CDevice(i2c,I2C_ADDRESS)

    # generate a good default gamma table
    self.channel_gamma_table = [SN3218.default_gamma_table for _ in range(18)]

    self.enable_leds(enable_mask)

  def _write_block(self, register, data):
    with self._i2c_device as i2c:
      i2c.write(bytes([register])+bytes(data))

  def enable(self):
    """Enable output."""
    self._write_block(CMD_ENABLE_OUTPUT, [0x01])

  def disable(self):
    """Disable output."""
    self._write_block(CMD_ENABLE_OUTPUT, [0x00])

  def reset(self):
    """Reset all internal registers."""
    self._write_block(CMD_RESET, [0xFF])

  def enable_leds(self, enable_mask):
    """Enable or disable each LED channel.

    The first 18 bit values are
    used to determine the state of each channel (1=on, 0=off) if fewer
    than 18 bits are provided the remaining channels are turned off.

    Args:
      enable_mask (int): up to 18 bits of data
    Raises:
      TypeError: if enable_mask is not an integer.
    """
    if not isinstance(enable_mask, int):
      raise TypeError("enable_mask must be an integer")

    self._write_block(CMD_ENABLE_LEDS, [
      enable_mask & 0x3F,
      (enable_mask >> 6) & 0x3F,
      (enable_mask >> 12) & 0X3F])
    self._write_block(CMD_UPDATE, [0xFF])

  def channel_gamma(self, channel, gamma_table):
    """Override the gamma table for a single channel.

    Args:
      channel (int): channel number
      gamma_table (list): list of 256 gamma correction values
    Raises:
      TypeError: if channel is not an integer.
      ValueError: if channel is not in the range 0..17.
      TypeError: if gamma_table is not a list.
    """
    if not isinstance(channel, int):
      raise TypeError("channel must be an integer")

    if channel not in range(18):
      raise ValueError("channel be an integer in the range 0..17")

    if not isinstance(gamma_table, list) or len(gamma_table) != 256:
      raise TypeError("gamma_table must be a list of 256 integers")

    self.channel_gamma_table[channel] = gamma_table

  def output(self, values):
    """Output a new set of values to the driver.

    Args:
      values (list): channel number
    Raises:
      TypeError: if values is not a list of 18 integers.
    """
    if not isinstance(values, list) or len(values) != 18:
      raise TypeError("values must be a list of 18 integers")

    self._write_block(CMD_SET_PWM_VALUES,
                      [self.channel_gamma_table[i][values[i]] for i in range(18)])
    self._write_block(CMD_UPDATE, [0xFF])

  def output_raw(self, values):
    """Output a new set of values to the driver.

    Similar to output(), but does not use channel_gamma_table.

    Args:
      values (list): channel number
    Raises:
      TypeError: if values is not a list of 18 integers.
    """
    if len(values) != 18:
      raise TypeError("values must be a list of 18 integers")

    self._write_block(CMD_SET_PWM_VALUES, values)
    self._write_block(CMD_UPDATE, [0xFF])

