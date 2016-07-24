### Author: EMF Badge team
### Description: Test app
### Category: Games
### License: MIT
### Appname: Partymode1
### Built-in: yes

import ugfx
import pyb
import buttons

buttons.init()

COLORS = [ugfx.RED, ugfx.GREEN, ugfx.YELLOW, ugfx.WHITE ,ugfx.BLUE]
i = 0

while not buttons.is_triggered("BTN_MENU"):
	i = (i + 1) % len(COLORS)
	ugfx.area(0,0,320,240, COLORS[i])
	pyb.delay(60)

pyb.hard_reset()