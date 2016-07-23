import ugfx
import pyb
import os
from database import *
from filesystem import *
import buttons
import gc
import stm


def draw(window):
	#ToDo: change to use window._____ rather than ugfx.____
	ugfx.set_default_font("D*")
	ugfx.text(40,40,"My name is...",ugfx.BLUE)
	ugfx.text(40,80,database_get("display-name", "<not set yet>"),ugfx.BLUE)
	ugfx.circle(140,150,40,ugfx.GREEN)
	ugfx.circle(160,150,40,ugfx.GREEN)
	ugfx.circle(180,150,40,ugfx.GREEN)
	
def draw_destroy(obj_name):
#there may be some .destroy() functions that could be wanted to be called
	pass