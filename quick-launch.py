import ugfx
import os

wi = ugfx.get_width()
hi = ugfx.get_height()

win_header = ugfx.Container(0,0,wi,30)
win_quick = ugfx.Container(0,33,int(2*wi/3),hi-2-33)
win_help = ugfx.Container(int(2*wi/3)+2,33,int(wi/3)-2,hi-33)


ugfx.set_default_font("D*")
title = ugfx.Label(3,3,wi-10,45,"EMF Camp 2016",win_header)


ugfx.set_default_font("c*")

btn_q2 = ugfx.Button(10,5,100,30,"Map",win_quick)
btn_q3 = ugfx.Button(10,40,100,30,"SMS",win_quick)
btn_q4 = ugfx.Button(10,75,100,30,"Snake",win_quick)
btn_q5 = ugfx.Button(10,110,100,30,"App Store",win_quick)
btn_q6 = ugfx.Button(10,145,100,30,"View All",win_quick)

btn_ok = ugfx.Button(10,win_help.get_height()-25,20,20,"A",win_help)
l_ok = ugfx.Label(35,win_help.get_height()-25,100,20,"Run",win_help)

btn_back = ugfx.Button(10,win_help.get_height()-50,20,20,"B",win_help)
l_back = ugfx.Label(35,win_help.get_height()-50,100,20,"Back",win_help)

btn_menu = ugfx.Button(10,win_help.get_height()-75,20,20,"M",win_help)
l_back = ugfx.Label(35,win_help.get_height()-75,100,20,"Menu",win_help)


win_header.show()
win_quick.show()
win_help.show()







def callback_up(line):
	global stay_here
	print("Up")

def callback_down(line):
	global stay_here
	print("Down")
	ugfx.send_tab()
	
def callback_menu(line):
	global stay_here
	stay_here = 0
	print("Quitting")

tgl_menu = pyb.Pin("BTN_MENU", pyb.Pin.IN)
extint1 = pyb.ExtInt(tgl_menu, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, callback_menu)
tgl_up = pyb.Pin("JOY_UP", pyb.Pin.IN)
extint2 = pyb.ExtInt(tgl_up, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, callback_up)
tgl_down = pyb.Pin("JOY_DOWN", pyb.Pin.IN)
extint3 = pyb.ExtInt(tgl_down, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, callback_down)

stay_here = 1;

while(stay_here):
	pyb.wfi()
extint1 = pyb.ExtInt(tgl_menu, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, None)
extint2 = pyb.ExtInt(tgl_up, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, None)
extint3 = pyb.ExtInt(tgl_down, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, None)

	
