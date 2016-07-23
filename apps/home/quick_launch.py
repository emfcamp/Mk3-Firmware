import ugfx
import os
import pyb
import buttons
import dialogs
from database import *
from filesystem import *

joy_updown = 0
joy_lr = 0


def callback_arrow_up(line):
	global joy_updown
	joy_updown = 1

def callback_arrow_down(line):
	global joy_updown
	joy_updown = -1

def callback_arrow_right(line):
	global joy_lr
	joy_lr = 1

def callback_arrow_left(line):
	global joy_lr
	joy_lr = -1

def _move_arrow(x,y,cursor_loc, win_quick):

	arrow = [[0,0],[20,7],[0,14],[4,7]]

	win_quick.fill_polygon(cursor_loc[0]*150+4, cursor_loc[1]*35+14, arrow ,ugfx.WHITE)

	cursor_loc[0] += x
	cursor_loc[1] += y

	if cursor_loc[0] < 0:
		cursor_loc[0] = 0
	if cursor_loc[0] > 1:
		cursor_loc[0] = 1

	if cursor_loc[1] < 0:
		cursor_loc[1] = 0
	if cursor_loc[1] > 3:
		cursor_loc[1] = 3

	win_quick.fill_polygon(cursor_loc[0]*150+4, cursor_loc[1]*35+14, arrow ,ugfx.RED)



wi = ugfx.width()
hi = ugfx.height()

win_header = ugfx.Container(0,0,wi,30)
win_quick = ugfx.Container(0,33,wi,hi-33-33)
win_help = ugfx.Container(0,hi-30,wi,30)

file_list = []

pinned = database_get("pinned", None)

if pinned == None:
	pinned = []
	print("List of pinned files doesn't exist, creating default")
	pinned.append("apps/snake/main.py")
	pinned.append("examples/party_mode.py")
	database_set("pinned", pinned)
	
file_list = pinned;
print(file_list)
file_name = []
for f in file_list:
	an = get_app_attribute(f,"Appname")
	if len(an) == 0:
		an = get_app_foldername(f)
	if (an == ""):
		file_name.append("???")
	else:
		file_name.append(an)


while len(file_list) < 8:
	file_list.append("")
	file_name.append("")
file_list[7] = "apps/home/file_loader.py"
file_name[7] = "View All"


ugfx.set_default_font("D*")
title = ugfx.Label(3,3,wi-10,45,"EMF Camp 2016",parent=win_header)

s = ugfx.Style()
s.set_focus(ugfx.RED)

ugfx.set_default_font("c*")
ugfx.set_default_style(s)

btn_c1r1 = ugfx.Button(25,5,100,30,file_name[0],parent=win_quick)
btn_c1r2 = ugfx.Button(25,40,100,30,file_name[1],parent=win_quick)
btn_c1r3 = ugfx.Button(25,75,100,30,file_name[2],parent=win_quick)
btn_c1r4 = ugfx.Button(25,110,100,30,file_name[3],parent=win_quick)

btn_c2r1 = ugfx.Button(180,5,100,30,file_name[4],parent=win_quick)
btn_c2r2 = ugfx.Button(180,40,100,30,file_name[5],parent=win_quick)
btn_c2r3 = ugfx.Button(180,75,100,30,file_name[6],parent=win_quick)
btn_c2r4 = ugfx.Button(180,110,100,30,file_name[7],parent=win_quick)


btn_ok = ugfx.Button(10,5,20,20,"A",parent=win_help,shape=ugfx.Button.ELLIPSE)
l_ok = ugfx.Label(40,5,100,20,"Run",parent=win_help)

btn_back = ugfx.Button(100,5,20,20,"B",parent=win_help,shape=ugfx.Button.ELLIPSE)
l_back = ugfx.Label(130,5,100,20,"Back",parent=win_help)

btn_menu = ugfx.Button(200,5,20,20,"M",parent=win_help,shape=ugfx.Button.ROUNDED)
l_back = ugfx.Label(230,5,100,20,"Menu",parent=win_help)


win_header.show()
win_quick.show()
win_help.show()



#enable_irq()
buttons.init()
buttons.enable_interrupt("JOY_UP", callback_arrow_up)
buttons.enable_interrupt("JOY_DOWN", callback_arrow_down)
buttons.enable_interrupt("JOY_LEFT", callback_arrow_left)
buttons.enable_interrupt("JOY_RIGHT", callback_arrow_right)

cursor_loc = [0, 0]

_move_arrow(0,0,cursor_loc, win_quick)

app_to_load = "home"

torun = "";

while True:
	pyb.wfi()

	if (joy_updown != 0) or (joy_lr != 0):
		_move_arrow(joy_lr, joy_updown, cursor_loc, win_quick)
		joy_updown = 0
		joy_lr = 0
		
	if buttons.is_triggered("BTN_B"):
		break;
		
	#if buttons.is_triggered("BTN_MENU"):
	#	open unpin dialog
	#	break;

	if buttons.is_triggered("BTN_A"):

		torun = file_list[cursor_loc[0]*4 + cursor_loc[1]]
		print(torun)
		if len(torun) > 3:
			if torun.endswith(".py"):
				break

buttons.disable_all_interrupt()

win_header.hide()
win_quick.hide()
win_help.hide()
btn_c1r1.destroy()
btn_c1r2.destroy()
btn_c1r3.destroy()
btn_c1r4.destroy()
btn_c2r1.destroy()
btn_c2r2.destroy()
btn_c2r3.destroy()
btn_c2r4.destroy()
btn_ok.destroy()
l_ok.destroy()
btn_back.destroy()
l_back.destroy()
btn_menu.destroy()
l_back.destroy()
win_header.destroy()
win_quick.destroy()
win_help.destroy()
title.destroy()

#deinit ugfx here

if len(torun) > 0:
	print("Running: " + torun)
	buttons.enable_menu_reset()
	#try:
	mod = __import__(torun[:-3])
	if "main" in dir(mod):
		mod.main()
	#except Exception as e:
	#	dialogs.notice(str(e), width=wi-20, height=hi-20)
	ugfx.area(0,0,ugfx.width(),ugfx.height(),0)
	#deinit ugfx here
	#could hard reset here too

#	execfile("apps/%s/main.py" % (app_to_load))
