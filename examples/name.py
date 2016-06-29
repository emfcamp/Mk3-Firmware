import ugfx
import pyb

def: display_name():
	ugfx.area(0,0,ugfx.get_width(),ugfx.get_height(),0xFFFF)
	ugfx.set_default_font("D*")
	ugfx.text(40,120,"MATT",ugfx.YELLOW)
	ugfx.circle(160,200,40,ugfx.GREEN)
	
display_name()