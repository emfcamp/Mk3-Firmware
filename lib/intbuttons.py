### Author: EMF Badge team
### Description: Convenience methods for dealing with the TiLDA buttons
### License: MIT

import pyb
import buttons

CONFIG = buttons.CONFIG

_button_state = {
	"JOY_UP": {"pressed":0, "released":1, "last_pressed":0},
	"JOY_DOWN": {"pressed":0, "released":1, "last_pressed":0},
	"JOY_RIGHT": {"pressed":0, "released":1, "last_pressed":0},
	"JOY_LEFT": {"pressed":0, "released":1, "last_pressed":0},
	"JOY_CENTER":  {"pressed":0, "released":1, "last_pressed":0},
	"BTN_MENU": {"pressed":0, "released":1, "last_pressed":0},
	"BTN_A":  {"pressed":0, "released":1, "last_pressed":0},
	"BTN_B": {"pressed":0, "released":1, "last_pressed":0}
}

_button_reverse = {
	15 : "BTN_A",
	11 : "BTN_B",
	3  : "BTN_MENU",
	0  : "JOY_CENTER",
	8  : "JOY_UP",
	10 : "JOY_RIGHT",
	6  : "JOY_LEFT",
	9  : "JOY_DOWN"
}

_tilda_pins = buttons._tilda_pins

def _get_pin(button):
	return buttons._get_pin(button)

def _button_state_change(line):
	global _button_reverse, _button_state, _tilda_interrupts
	if buttons.is_pressed(_button_reverse[line]):
		_button_state[_button_reverse[line]]["pressed"] = pyb.millis()
		try:
			if _tilda_interrupts[_button_reverse[line]][1]:
				_tilda_interrupts[_button_reverse[line]][0](line)
		except KeyError:
			pass
	else:
		_button_state[_button_reverse[line]]["released"] = pyb.millis()
		try:
			if _tilda_interrupts[_button_reverse[line]][2]:
				_tilda_interrupts[_button_reverse[line]][0](line)
		except KeyError:
			pass

def init(buttons = CONFIG.keys()):
	"""Inits all pins used by the TiLDA badge"""
	global _tilda_pins, _tilda_interrupts

	if _tilda_interrupts is None:
		_tilda_interrupts = {}

	for button in buttons:
		_tilda_pins[button] = pyb.Pin(button, pyb.Pin.IN)
		_tilda_pins[button].init(pyb.Pin.IN, CONFIG[button])
		if not buttons.has_interrupt(button):
			buttons.enable_interrupt(button, _button_state_change, True, True)

def is_pressed(button):
	if (_button_state[button]["pressed"] > _button_state[button]["released"]):
		return True
	return False

def is_triggered(button, interval = 30):
	# if the button is currently being pressed, and was pressed sometime in the past 30 milliseconds
	if (is_pressed(button) and (_button_state[button]["pressed"] + interval) > pyb.millis()):
		return True
	return False
