import ugfx
import pyb
import os
from database import *
from filesystem import *
import buttons
import gc
import stm

obj = []

def draw(x,y,window):
	#ToDo: change to use window._____ rather than ugfx.____
	sty = ugfx.Style()
	sty.set_enabled([ugfx.WHITE, ugfx.BLACK, ugfx.WHITE, ugfx.WHITE])
	win2 = ugfx.Container(x,y,window.width(),window.height(),sty)
	obj.append(win2)
	#ugfx.Imagebox(0,0,window.width(),window.height(),"apps/home/back.bmp",0, win2)
	ugfx.set_default_font(ugfx.FONT_NAME)
	l=ugfx.Label(5,20,310,window.height()-20,database_get("display-name", "<not actually set yet>"),parent=win2)
	obj.append(l)
	ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
	obj.append(ugfx.Label(5,0,310,20,"My name is...",parent=win2))
	#ugfx.text(40,80,database_get("display-name", "<not set yet>"),ugfx.BLUE)
	#ugfx.circle(140,150,40,ugfx.GREEN)
	#ugfx.circle(160,150,40,ugfx.GREEN)
	#ugfx.circle(180,150,40,ugfx.GREEN)
	win2.show()
	
def draw_destroy(obj_name):
#there may be some .destroy() functions that could be wanted to be called
	for o in obj:
		o.destroy()
