import ugfx
from badge import Badge
import pyb

def prompt_boolean(text, true_text="Yes", false_text="No"):
	"""A simple two-options dialog"""
	width = int(ugfx.width() * 2 / 3)
	height = int(ugfx.height() / 2)

	window = ugfx.Container(int(ugfx.width()/6), int(ugfx.height()/4), width, height)
	button_yes = ugfx.Button(int(width/12), int(height*3/5), int(width/3), int(height/5), "A: " + true_text, window)
	button_no = ugfx.Button(int(width/2 + width/12), int(height*3/5), int(width/3), int(height/5),"B: " + false_text, window)
	label = ugfx.Label(int(width/10), int(height/10), int(width*4/5), int(height*2/5), text, window)

	try:
		badge = Badge()
		badge.init_pins()

		button_yes.attach_input(ugfx.BTN_A)
		button_no.attach_input(ugfx.BTN_B)

		window.show()

		while True:
			pyb.wfi()
			if badge.is_pressed("BTN_A"): return True
			if badge.is_pressed("BTN_B"): return False

	finally:
		window.hide()
		window.destroy()
		button_yes.destroy()
		button_no.destroy()
		label.destroy()

def prompt_text(description, default=""):
	"""Shows a dialog and keyboard that allows the user to input/change a string"""
	# ToDo: Actually show dialog
	return default
