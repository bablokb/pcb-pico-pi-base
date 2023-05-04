import dothat.backlight as backlight
import dothat.lcd as lcd

# Reset the LED states and polarity
backlight.graph_off()

# Empty the screen
lcd.clear()

# Turn off the backlight
backlight.rgb(0, 0, 0)
