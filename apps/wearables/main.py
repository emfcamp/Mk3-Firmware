### Author: Bob Clough
### Description: Wearables Controller
### Category: Flashy
### License: MIT
### Appname : Wearables
### Built-in: no

import ugfx
from database import *
import dialogs
import buttons

buttons.init()
buttons.disable_menu_reset()

ugfx.init()
ugfx.clear(ugfx.html_color(0x7c1143))

def tick_inc(t):
	global ugfx
	ugfx.poll()

menu_items = [
	{"title": "Rainbow", "value":"rainbow"},
	{"title": "Matrix", "value":"matrix"},
	{"title": "Colour", "value":"colour"}
]

led_seq_name = database_get("led-seq-name", "rainbow")

option = dialogs.prompt_option(menu_items, text="What sequence do you want?", title="Wearables Controller")

if option:
	database_set("led-seq-name", option['value'])

	timer = pyb.Timer(3)
	timer.init(freq=60)
	timer.callback(tick_inc)

	led_count = database_get("led-count", "1")
	count = None

	ugfx.clear(ugfx.html_color(0x7c1143))

	while True:
		count = dialogs.prompt_text("How many LEDs? (Numeric)", default=str(led_count))
		print (type(count), count)
		if count.isdigit():
			count = int(count)
			break

	database_set("led-count", count)

	if option['value'] == "rainbow":
		timer.deinit()
		rainbow_speeds = [
			{"title": "Normal", "value":100},
			{"title": "Fast", "value":20},
			{"title": "Slow", "value":500}
		]
		led_seq_name = database_get("led-period", "rainbow")

		speed = dialogs.prompt_option(rainbow_speeds, text="How fast?", title="Rainboooooowwwww")

		if speed:
			database_set("led-period", speed['value'])

	elif option['value'] == "matrix":
		database_set("led-period", 500)
	elif option['value'] == "colour":
		database_set("led-period", 1000)

		led_colour = database_get("led-colour", "#ffffff")

		ugfx.clear(ugfx.html_color(0x7c1143))

		colourstring = dialogs.prompt_text("What Colour (HTML Colour Code)", default=led_count)
		colourstring = colourstring.strip()
		if colourstring[0] == '#':
			colourstring = colourstring[1:]
		r, g, b = colourstring[:2], colourstring[2:4], colourstring[4:]
		r, g, b = [int(n, 16) for n in (r, g, b)]
		colour = "#%02X%02X%02X" % (r, g, b)

		database_set("led-colour", colour)
