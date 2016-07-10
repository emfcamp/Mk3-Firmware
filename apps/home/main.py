import ugfx
import pyb
from database import *
import buttons

def display_name():
	ugfx.area(0,0,ugfx.width(),ugfx.height(),0xFFFF)
	ugfx.set_default_font("D*")
	ugfx.text(40,90,"My name is...",ugfx.BLUE)
	ugfx.text(40,120,database_get("name", "<not set yet>"),ugfx.BLUE)
	ugfx.circle(140,200,40,ugfx.GREEN)
	ugfx.circle(160,200,40,ugfx.GREEN)
	ugfx.circle(180,200,40,ugfx.GREEN)

def button_press():
	import apps.home.quick_launch
	apps.home.quick_launch.main()

ugfx.init()
display_name()

buttons.init()

while True:
	pyb.wfi()
	if buttons.is_triggered("BTN_MENU"):
		button_press()
