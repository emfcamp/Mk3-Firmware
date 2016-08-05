### Author: EMF Badge team
### Description: Test app for the hook into the home screen
### Category: Example
### License: MIT
### Appname : Home Callback Test

import ugfx, buttons, pyb

ugfx.init()
buttons.init()
ugfx.clear()

ugfx.Label(5, 5, ugfx.width(), ugfx.height(), "Nothing to see here")

while True:
	pyb.wfi()