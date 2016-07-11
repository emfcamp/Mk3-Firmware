import ugfx
import pyb


keepgoing = 1
tgl_menu = pyb.Pin("BTN_MENU", pyb.Pin.IN)
tgl_menu.init(pyb.Pin.IN, pyb.Pin.PULL_UP)
ugfx.enable_tear()
tear = pyb.Pin("TEAR", pyb.Pin.IN)
wi = ugfx.width()
hi = ugfx.height()
while(keepgoing):
	
	while(tear.value() == 0):
		2+2 
	while(tear.value()):
		2+2 
	ugfx.area(0,0,wi,hi,ugfx.RED)
	pyb.delay(60)
	
	while(tear.value() == 0):
		2+2 
	while(tear.value()):
		2+2 
	ugfx.area(0,0,wi,hi,ugfx.GREEN)
	pyb.delay(60)
	
	while(tear.value() == 0):
		2+2 
	while(tear.value()):
		2+2 
	ugfx.area(0,0,wi,hi,ugfx.YELLOW)
	pyb.delay(60)
	
	while(tear.value() == 0):
		2+2 
	while(tear.value()):
		2+2 
	ugfx.area(0,0,wi,hi,ugfx.WHITE)
	pyb.delay(60)
	
	while(tear.value() == 0):
		2+2 
	while(tear.value()):
		2+2 
	ugfx.area(0,0,wi,hi,ugfx.BLUE)
	pyb.delay(60)
		
	if tgl_menu.value() == 0:
		keepgoing = 0
ugfx.disable_tear()