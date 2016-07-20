import ugfx
import pyb
import os
from database import *
import buttons
import gc

def display_name():
	ugfx.area(0,0,ugfx.width(),ugfx.height(),0xFFFF)
	ugfx.set_default_font("D*")
	ugfx.text(40,90,"My name is...",ugfx.BLUE)
	ugfx.text(40,120,database_get("name", "<not set yet>"),ugfx.BLUE)
	ugfx.circle(140,200,40,ugfx.GREEN)
	ugfx.circle(160,200,40,ugfx.GREEN)
	ugfx.circle(180,200,40,ugfx.GREEN)

while True:
	ugfx.init()
	display_name()

	buttons.init()
	
	gc.collect()

	while not buttons.is_triggered("BTN_MENU"):
		pyb.wfi()

	## ToDo: Maybe boot should always chdir to the app folder?
	execfile("apps/home/quick_launch.py")
	
