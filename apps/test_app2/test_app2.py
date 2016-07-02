import ugfx
import pyb

def main():
	keepgoing = 1
	tgl_menu = pyb.Pin("BTN_MENU", pyb.Pin.IN)
	tgl_menu.init(pyb.Pin.IN, pyb.Pin.PULL_UP)
	while(keepgoing):
		ugfx.area(0,0,320,240,ugfx.RED)
		pyb.delay(600)
		if tgl_menu.value() == 0:
			keepgoing = 0
		ugfx.area(0,0,320,240,ugfx.GREEN)
		pyb.delay(600)
		if tgl_menu.value() == 0:
			keepgoing = 0
		ugfx.area(0,0,320,240,ugfx.YELLOW)
		pyb.delay(600)
		if tgl_menu.value() == 0:
			keepgoing = 0
		ugfx.area(0,0,320,240,ugfx.WHITE)
		pyb.delay(600)
		if tgl_menu.value() == 0:
			keepgoing = 0
		ugfx.area(0,0,320,240,ugfx.BLUE)
		pyb.delay(600)
		if tgl_menu.value() == 0:
			keepgoing = 0