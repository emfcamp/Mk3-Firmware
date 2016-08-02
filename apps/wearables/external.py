import database
import pyb
from apps.wearables.colour import Colour

def Wheel(pos):
	position = 255 - pos

	if (position < 85):
			return (255 - position * 3, 0, position * 3)

	if (position < 170):
			position = position - 85
			return (0, position * 3, 255 - position * 3)

	position = position - 170
	return (position * 3, 255 - position * 3, 0)

	return value

def tick():
	global wheelColour, ledcount, sequence, ledpin

	pin = pyb.Pin(ledpin)
	neo = pyb.Neopix(pin)

	leds = [0x000000] * ledcount

	if (sequence == "rainbow"):
		wheelColour = (wheelColour + 8) & 255
		for ledNumber in range(0, ledcount):
			pos = ((ledNumber*8)+wheelColour)
			pos = pos & 255
			leds[ledNumber] = int("%02X%02X%02X" % Wheel(pos), 16)
	elif (sequence == "matrix"):
		for ledNumber in range(0, ledcount):
			led_green = (pyb.rng() & 255)
			led_colour = Colour(0, led_green, 0)
			if led_green < 230:
				led_colour.set_g(int(led_green / 8))
			if led_green > 253:
				led_colour.set_hex('#ffffff')
			leds[ledNumber] = led_colour.get_neo()
	elif (sequence == "colour"):
		colour = database.database_get("led-colour", "#ffffff")
		tmp_colour = Colour()
		tmp_colour.set_hex(colour)
		leds = [tmp_colour.get_neo()] * ledcount
	neo.display(leds)

# 67 LEDs because thats how many i have on my lanyard
ledcount = database.database_get("led-count", 67)
# show the rainbow sequence by default
sequence = database.database_get("led-seq-name", "rainbow")
# default to pb13, which is the onboard neopixel
ledpin = database.database_get("led-port", "PB13")

wheelColour = 0
period = database.database_get("led-period", 50)
