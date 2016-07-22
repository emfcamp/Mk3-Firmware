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
	ugfx.text(40,120,database_get("display-name", "<not set yet>"),ugfx.BLUE)
	ugfx.circle(140,200,40,ugfx.GREEN)
	ugfx.circle(160,200,40,ugfx.GREEN)
	ugfx.circle(180,200,40,ugfx.GREEN)
	
def draw_battery(x,y,back_colour,percent):
	ugfx.set_default_font("c*")	
	ugfx.text(x+35,y,str(int(percent)),back_colour^0xFFFF)	
	y += 2
	ugfx.area(x,y,30,11,back_colour^0xFFFF)
	ugfx.area(x+30,y+3,3,5,back_colour^0xFFFF)	
	ugfx.area(x+2,y+2,26,7,back_colour)
	ugfx.area(x+2,y+2,int(percent*26/100),7,back_colour^0xFFFF)

tick = 0;
	
def tick_inc():
	global tick
	tick += 1
	
def backlight_adjust():
	l = pyb.ADC(16).read()
	if (l > 90):
		ugfx.backlight(100)
	elif (l > 20):
		ugfx.backlight(70)
	else:
		ugfx.backlight(30)




while True:
	ugfx.init()
	display_name()

	buttons.init()
	
	gc.collect()
	
	draw_battery(3,3,0xFFFF,49)
	
	timerb = pyb.Timer(16)
	timerb.init(freq=1)
	timerb.callback(tick_inc())
	
	while True:
		pyb.wfi()
		
		if tick > 0:
			tick = 0
			backlight_adjust()
			draw_battery(3,3,0xFFFF,49)

		if buttons.is_triggered("BTN_MENU"):
			break
		
		
	timerb.deinit()
	ugfx.backlight(100)

	## ToDo: Maybe boot should always chdir to the app folder?
	execfile("apps/home/quick_launch.py")
	
