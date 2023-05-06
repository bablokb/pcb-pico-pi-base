import dothat.lcd as lcd
from secrets import secrets
import wifi

# Clear the LCD
lcd.clear()
lcd.write(f"connecting to")
lcd.set_cursor_position(column=0,row=1)
lcd.write(f"{secrets.ssid}")

# connect
if not hasattr(secrets,'channel'):
  secrets.channel = 0
if not hasattr(secrets,'timeout'):
  secrets.timeout = None

try:
  wifi.radio.connect(secrets.ssid,
                     secrets.password,
                     channel = secrets.channel,
                     timeout = secrets.timeout
                     )
  lcd.clear()
  lcd.write(f"connected")
  lcd.set_cursor_position(column=0,row=1)
  lcd.write(f"{wifi.radio.ipv4_address}")
  lcd.set_cursor_position(column=0,row=2)
  lcd.write(f"{wifi.radio.hostname}")
except:
  lcd.clear()
  lcd.write(f"failed")
