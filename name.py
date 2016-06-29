import ugfx
import pyb

def display_name():
	ugfx.area(0,0,ugfx.width(),ugfx.height(),0xFFFF)
	ugfx.set_default_font("D*")
	ugfx.text(40,120,"MATT",ugfx.YELLOW)
	ugfx.circle(160,200,40,ugfx.GREEN)
	
def button_press():
	extint1 = pyb.ExtInt(tgl_menu, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, None)
	
	import quick_launch
	quick_launch.main()
	
	extint1 = pyb.ExtInt(tgl_menu, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, button_press)	
	display_name()

	
display_name()

tgl_menu = pyb.Pin("BTN_MENU", pyb.Pin.IN)
tgl_menu.init(pyb.Pin.IN, pyb.Pin.PULL_UP)
#extint1 = pyb.ExtInt(tgl_menu, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, button_press)
while True:
	pyb.wfi()
	if tgl_menu.value() == 0:
		button_press()