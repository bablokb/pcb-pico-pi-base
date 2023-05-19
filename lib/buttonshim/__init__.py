# ----------------------------------------------------------------------------
# CircuitPython version of the Linux-driver provided by Pimoroni.
# (https://github.com/pimoroni/button-shim)
# ----------------------------------------------------------------------------

import time
import busio
from adafruit_bus_device.i2c_device import I2CDevice

DEFAULT_ADDR = 0x3f
LED_DATA = 7
LED_CLOCK = 6

REG_INPUT = 0x00
REG_OUTPUT = 0x01
REG_POLARITY = 0x02
REG_CONFIG = 0x03

NUM_BUTTONS = 5

NAMES = ['A', 'B', 'C', 'D', 'E']
"""Sometimes you want to print the plain text name of the button that's triggered.

You can use::

    buttonshim.NAMES[button_index]

To accomplish this.

"""

ERROR_LIMIT = 10

FPS = 60

LED_GAMMA = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
    2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5,
    6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 11, 11,
    11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18,
    19, 19, 20, 21, 21, 22, 22, 23, 23, 24, 25, 25, 26, 27, 27, 28,
    29, 29, 30, 31, 31, 32, 33, 34, 34, 35, 36, 37, 37, 38, 39, 40,
    40, 41, 42, 43, 44, 45, 46, 46, 47, 48, 49, 50, 51, 52, 53, 54,
    55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
    71, 72, 73, 74, 76, 77, 78, 79, 80, 81, 83, 84, 85, 86, 88, 89,
    90, 91, 93, 94, 95, 96, 98, 99, 100, 102, 103, 104, 106, 107, 109, 110,
    111, 113, 114, 116, 117, 119, 120, 121, 123, 124, 126, 128, 129, 131, 132, 134,
    135, 137, 138, 140, 142, 143, 145, 146, 148, 150, 151, 153, 155, 157, 158, 160,
    162, 163, 165, 167, 169, 170, 172, 174, 176, 178, 179, 181, 183, 185, 187, 189,
    191, 193, 194, 196, 198, 200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220,
    222, 224, 227, 229, 231, 233, 235, 237, 239, 241, 244, 246, 248, 250, 252, 255]


class Handler():
  def __init__(self):
    self.press = None
    self.release = None
    self.t_pressed = 0
    self.t_repeat = 0

_handlers = [Handler() for x in range(NUM_BUTTONS)]

class ButtonShim():
  BUTTON_A = 0
  """Button A"""
  BUTTON_B = 1
  """Button B"""
  BUTTON_C = 2
  """Button C"""
  BUTTON_D = 3
  """Button D"""
  BUTTON_E = 4
  """Button E"""
  def __init__(self, i2c, i2c_addr=DEFAULT_ADDR):
    self.i2c_addr   = i2c_addr
    self.i2c_device = I2CDevice(i2c,i2c_addr)

    # The LED is an APA102 driven via the i2c IO expander.
    # We must set and clear the Clock and Data pins
    # Each byte in _reg_queue represents a snapshot of the pin state

    self._errors = 0
    self._led_data = []
    self._brightness = 0.5
    self._states = 0b00011111
    self._last_states = 0b00011111

    self._write_byte(REG_CONFIG, 0b00011111)
    self._write_byte(REG_POLARITY, 0b00000000)
    self._write_byte(REG_OUTPUT, 0b00000000)

    self._handlers = [Handler() for x in range(NUM_BUTTONS)]
    self.set_pixel(0, 0, 0)

  def _write_byte(self, register, value):
    with self.i2c_device as i2c:
      i2c.write(bytes([register])+bytes([value]))

  def _write_block(self, register, data):
    with self.i2c_device as i2c:
      i2c.write(bytes([register])+data)

  def _read_byte(self, register):
    return self._read_block(register,1)

  def _read_block(self, register, length):
    result = bytearray(length)
    with self.i2c_device as i2c:
      i2c.write_then_readinto(bytes([register]), result)
      return result
    return None

  def _set_bit(self,pin,value):
    if value:
      self._led_data[-1] |= (1 << pin)
    else:
      self._led_data[-1] &= ~(1 << pin)

  def _next(self):
    if len(self._led_data) == 0:
      self._led_data = [0b00000000]
    else:
      self._led_data.append(self._led_data[-1])
  
  def _write_byte_io(self,byte):
    for x in range(8):
      self._next()
      self._set_bit(LED_CLOCK, 0)
      self._set_bit(LED_DATA, byte & 0b10000000)
      self._next()
      self._set_bit(LED_CLOCK, 1)
      byte <<= 1

  def _update_led(self):
    """ update led-state """
    try:
      if self._led_data:
        for i in range(0,len(self._led_data)+1,32):
          chunk = self._led_data[i:i+32]
          self._write_block(REG_OUTPUT,bytes(chunk))
    except:
      raise
      self._errors += 1
      if self._errors > ERROR_LIMIT:
        raise RuntimeError(f"More than {ERROR_LIMIT} IO errors have occurred!")

  def set_brightness(self,brightness):
    if not isinstance(brightness, int) and not isinstance(brightness, float):
      raise ValueError("Brightness should be an int or float")
    if brightness < 0.0 or brightness > 1.0:
      raise ValueError("Brightness should be between 0.0 and 1.0")
    self._brightness = brightness
  
  def set_pixel(self,r,g,b):
    """Set the Button SHIM RGB pixel
  
    Display an RGB colour on the Button SHIM pixel.
  
    :param r: Amount of red, from 0 to 255
    :param g: Amount of green, from 0 to 255
    :param b: Amount of blue, from 0 to 255
  
    You can use HTML colours directly with hexadecimal notation in Python. EG::
  
    buttonshim.set_pixel(0xFF, 0x00, 0xFF)
  
    """
  
    if not isinstance(r, int) or r < 0 or r > 255:
      raise ValueError("Argument r should be an int from 0 to 255")
    if not isinstance(g, int) or g < 0 or g > 255:
      raise ValueError("Argument g should be an int from 0 to 255")
    if not isinstance(b, int) or b < 0 or b > 255:
      raise ValueError("Argument b should be an int from 0 to 255")

    r, g, b = [int(x * self._brightness) for x in (r, g, b)]
  
    self._write_byte_io(0)
    self._write_byte_io(0)
    self._write_byte_io(0b11101111)
    self._write_byte_io(LED_GAMMA[b & 0xff])
    self._write_byte_io(LED_GAMMA[g & 0xff])
    self._write_byte_io(LED_GAMMA[r & 0xff])
    self._write_byte_io(0)
    self._write_byte_io(0)
    self._update_led()

  def poll(self):
    """ update state of LEDs and query state of buttons """

    try:
      _states = self._read_byte(REG_INPUT)[0]
    except:
      self._errors += 1
      if self._errors > ERROR_LIMIT:
        raise RuntimeError(f"More than {ERROR_LIMIT} IO errors have occurred!")

    for x in range(NUM_BUTTONS):
      last = (self._last_states >> x) & 1
      curr = (_states >> x) & 1
      handler = self._handlers[x]
  
      # If last > curr then it's a transition from 1 to 0
      # since the buttons are active low, that's a press event
      if last > curr:
        handler.t_pressed = time.time()

        if callable(handler.press):
          handler.t_repeat = time.time()
          handler.press(x,True)
        continue

      if last < curr and callable(handler.release):
        handler.release(x,True)
        continue

    self._last_states = _states

    def on_hold(self,buttons, handler=None, hold_time=2):
      """Attach a hold handler to one or more buttons.
  
      This handler is fired when you hold a button for hold_time seconds.
  
      When fired it will run in its own Thread.
  
      It will be passed one argument, the button index::
  
          @buttonshim.on_hold(buttonshim.BUTTON_A)
          def handler(button):
              # Your code here
  
      :param buttons: A single button, or a list of buttons
      :param handler: Optional: a function to bind as the handler
      :param hold_time: Optional: the hold time in seconds (default 2)
  
      """
  
      if buttons is None:
        buttons = [BUTTON_A, BUTTON_B, BUTTON_C, BUTTON_D, BUTTON_E]
  
      if isinstance(buttons, int):
        buttons = [buttons]
  
      def attach_handler(handler):
        for button in buttons:
          self._handlers[button].hold = handler
          self._handlers[button].hold_time = hold_time
  
      if handler is not None:
        attach_handler(handler)
      else:
        return attach_handler
  
  def on_press(self,buttons, handler=None, repeat=False, repeat_time=0.5):
    """Attach a press handler to one or more buttons.
     This handler is fired when you press a button.
     When fired it will be run in its own Thread.
     It will be passed two arguments, the button index and a
    boolean indicating whether the button has been pressed/released::
         @buttonshim.on_press(buttonshim.BUTTON_A)
        def handler(button, pressed):
            # Your code here
     :param buttons: A single button, or a list of buttons
    :param handler: Optional: a function to bind as the handler
    :param repeat: Optional: Repeat the handler if the button is held
    :param repeat_time: Optional: Time, in seconds, after which to repeat
     """
  
    if buttons is None:
      buttons = [BUTTON_A, BUTTON_B, BUTTON_C, BUTTON_D, BUTTON_E]
  
    if isinstance(buttons, int):
      buttons = [buttons]
  
    def attach_handler(handler):
      for button in buttons:
        self._handlers[button].press = handler
        self._handlers[button].repeat = repeat
        self._handlers[button].repeat_time = repeat_time
  
    if handler is not None:
      attach_handler(handler)
    else:
      return attach_handler
  
  def on_release(self,buttons=None, handler=None):
    """Attach a release handler to one or more buttons.
     This handler is fired when you let go of a button.
     When fired it will be run in its own Thread.
     It will be passed two arguments, the button index and a
    boolean indicating whether the button has been pressed/released::
         @buttonshim.on_release(buttonshim.BUTTON_A)
        def handler(button, pressed):
            # Your code here
     :param buttons: A single button, or a list of buttons
    :param handler: Optional: a function to bind as the handler
     """
  
    if buttons is None:
      buttons = [BUTTON_A, BUTTON_B, BUTTON_C, BUTTON_D, BUTTON_E]
  
    if isinstance(buttons, int):
      buttons = [buttons]
  
    def attach_handler(handler):
      for button in buttons:
        self._handlers[button].release = handler

    if handler is not None:
      attach_handler(handler)
    else:
      return attach_handler
