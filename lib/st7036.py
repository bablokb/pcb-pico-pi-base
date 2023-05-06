# ----------------------------------------------------------------------------
# CircuitPython version of the Linux-driver provided by Pimoroni.
# (https://github.com/pimoroni/st7036)
# ----------------------------------------------------------------------------

import time

import board
import time
import busio
import digitalio
from adafruit_bus_device.spi_device import SPIDevice

__version__ = '1.4.4'

COMMAND_CLEAR = 0b00000001
COMMAND_HOME = 0b00000010
COMMAND_SCROLL = 0b00010000
COMMAND_DOUBLE = 0b00010000
COMMAND_BIAS = 0b00010100
COMMAND_SET_DISPLAY_MODE = 0b00001000

BLINK_ON = 0b00000001
CURSOR_ON = 0b00000010
DISPLAY_ON = 0b00000100
TOP = 1
BOTTOM = 0

class st7036():
  def __init__(self,
               cs_register,
               reset_pin=None,
               rows=3,
               columns=16,
               cs_spi=board.CE0,
               instruction_set_template=0b00111000):
    
    self._reset_pin = None
    if reset_pin is not None:
      self._reset_pin  = digitalio.DigitalInOut(reset_pin)
      self._reset_pin.direction  = digitalio.Direction.OUTPUT
      self.reset()

    self.row_offsets = ([0x00], [0x00, 0x40], [0x00, 0x10, 0x20])[rows - 1]
    self.rows = rows
    self.columns = columns

    self._cs_spi            = digitalio.DigitalInOut(cs_spi)
    self._cs_spi.direction  = digitalio.Direction.OUTPUT

    spi = busio.SPI(board.SCLK,board.MOSI,board.MISO)
    self._spi = SPIDevice(spi,self._cs_spi)

    self._cs_register            = digitalio.DigitalInOut(cs_register)
    self._cs_register.direction  = digitalio.Direction.OUTPUT

    self.instruction_set_template = instruction_set_template

    self._enabled = True
    self._cursor_enabled = False
    self._cursor_blink = False
    self._double_height = 0

    self.animations = [None] * 8

    self.update_display_mode()

    # set entry mode (no shift, cursor direction)
    self._write_command(0b00000100 | 0b00000010)

    self.set_bias(1)

    self.set_contrast(40)
    self.clear()

  def reset(self):
    if self._reset_pin is not None:
      self._reset_pin.value = False
      time.sleep(0.001)
      self._reset_pin.value = True

  def set_bias(self, bias=1):
    self._write_command(COMMAND_BIAS | (bias << 4) | 1, 1)

  def set_contrast(self, contrast):
    """
    Sets the display contrast.

    Args:
      contrast (int): contrast value
    Raises:
      TypeError: if contrast is not an int
      ValueError: if contrast is not in the range 0..0x3F
    """
    if type(contrast) is not int:
      raise TypeError("contrast must be an integer")

    if contrast not in range(0, 0x40):
      raise ValueError("contrast must be an integer in the range 0..0x3F")

    # For 3.3v operation the booster must be on, which is
    # on the same command as the (2-bit) high-nibble of contrast
    self._write_command((0b01010100 | ((contrast >> 4) & 0x03)), 1)
    self._write_command(0b01101011, 1)

    # Set low-nibble of the contrast
    self._write_command((0b01110000 | (contrast & 0x0F)), 1)

  def set_display_mode(self, enable=True, cursor=False, blink=False):
    """
    Sets the display mode.

    Args:
      enable (boolean): enable display output
      cursor (boolean): show cursor
      blink (boolean): blink cursor (if shown)
    """
    self._enabled = enable
    self._cursor_enabled = cursor
    self._cursor_blink = blink
    self.update_display_mode()

  def update_display_mode(self):
    mask = COMMAND_SET_DISPLAY_MODE
    mask |= DISPLAY_ON if self._enabled else 0
    mask |= CURSOR_ON if self._cursor_enabled else 0
    mask |= BLINK_ON if self._cursor_blink else 0
    self._write_command(mask)

  def enable_cursor(self, cursor=False):
    self._cursor_enabled = cursor
    self.update_display_mode()

  def enable_blink(self, blink=False):
    self._cursor_blink = blink
    self.update_display_mode()

  def set_cursor_offset(self, offset):
    """
    Sets the cursor position in DRAM

    Args:
      offset (int): DRAM offset to place cursor
    """
    self._write_command(0b10000000 | offset)

  def set_cursor_position(self, column, row):
    """
    Sets the cursor position in DRAM based on
    a row and column offset

    Args:
      column (int): column to move the cursor to
      row (int): row to move the cursor to
    Raises:
      ValueError: if row and column are not within defined screen size
    """
    if row not in range(self.rows) or column not in range(self.columns):
      raise ValueError("row and column must integers within the defined screen size")

    offset = self.row_offsets[row] + column

    self._write_command(0b10000000 | offset)

    time.sleep(0.0015)  # Allow at least 1.08ms for command to execute

  def home(self):
    """
    Sets the cursor position to 0,0
    """
    self.set_cursor_position(0, 0)

  def clear(self):
    """
    Clears the display and resets the cursor.
    """
    self._write_command(COMMAND_CLEAR)
    time.sleep(0.0015)  # Allow at least 1.08ms for clear command to execute
    self.home()

  def write(self, value):
    """
    Write a string to the current cursor position.

    Args:
      value (string): The string to write
    """
    self._cs_register.value = 1
    for i in [ord(char) for char in value]:
      self._write_spi([i])
      time.sleep(0.00005)

  def create_animation(self, anim_pos, anim_map, frame_rate):
    """Creates an animation in a given custom character slot

    Args:
      anim_pos (int): Character slot from 0 to 7 where current animation frame should be store on LCD
      anim_map: A list of custom character definitions. Each definition should be a list of 8 bytes describing the custom character for that frame,
      frame_rate: Speed of animation in frames-per-second
    """
    if anim_pos >= len(self.animations):
      raise ValueError("Valid animation positions are 0 to 7")

    if type(anim_map) is not list:
      raise ValueError("Animation map should be a list of animation frames")

    if type(anim_map[0]) is not list or len(anim_map[0]) < 8:
      raise ValueError("Animation frames should be lists of 8 bytes")

    self.create_char(anim_pos, anim_map[0])
    self.animations[anim_pos] = [anim_map, frame_rate]

  def update_animations(self):
    for i, animation in enumerate(self.animations):
      if animation is not None and len(animation) == 2:
        anim = animation[0]
        fps = animation[1]
        frame = anim[int(round(time.time() * fps) % len(anim))]
        self.create_char(i, frame)

  def create_char(self, char_pos, char_map):
    if char_pos < 0 or char_pos > 7:
      return False

    baseAddress = char_pos * 8
    for i in range(0, 8):
      self._write_command((0x40 | (baseAddress + i)))
      self._write_char(char_map[i])

    self.home()

  def cursor_left(self):
    self._write_command(COMMAND_SCROLL, 0)

  def cursor_right(self):
    self._write_command(COMMAND_SCROLL | (1 << 2), 0)

  def shift_left(self):
    self._write_command(COMMAND_SCROLL | (1 << 3), 0)  # 0x18

  def shift_right(self):
    self._write_command(COMMAND_SCROLL | (1 << 3) | (1 << 2), 0)  # 0x1C

  def double_height(self, enable=0, position=1):
    self._double_height = enable
    #self._write_instruction_set(0)    # ??!
    self._write_command(COMMAND_DOUBLE | (position << 3), 2)

  def _write_char(self, value):
    self._cs_register.value = 1
    self._write_spi([value])
    time.sleep(0.0001)

  def _write_instruction_set(self, instruction_set=0):
    self._cs_register.value = 0
    self._write_spi([self.instruction_set_template | instruction_set | (self._double_height << 2)])
    time.sleep(0.00006)

  def _write_command(self, value, instruction_set=0):
    self._cs_register.value = 0
    # select correct instruction set
    self._write_instruction_set(instruction_set)
    # switch to command-mode
    self._write_spi([value])
    time.sleep(0.00006)

  def _write_spi(self,value):
    with self._spi as spi:
      spi.write(bytes(value))
