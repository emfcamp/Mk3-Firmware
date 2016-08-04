import ugfx
import os
import pyb
import buttons
import dialogs
from database import *
from filesystem import *
import sys
import uio
import gc
import onboard
import dialogs

joy_updown = 0
joy_lr = 0

ugfx.init()
ugfx.clear(ugfx.html_color(0xA66FB0))

def _draw_cursor (x, y, color, win_quick):
	win_quick.fill_polygon(10 + x * 155, 15 + y * 40, [[0,0],[20,7],[0,14],[4,7]], color)

wi = ugfx.width()
hi = ugfx.height()

win_header = ugfx.Container(0,0,wi,30)
win_quick = ugfx.Container(0,33,wi,hi-33-33)
win_help = ugfx.Container(0,hi-30,wi,30)

file_list = []

pinned = database_get("pinned", ["app_library", "sponsors"])[:7]

if pinned == None:
	pinned = []
	print("List of pinned files doesn't exist, creating default")
	pinned.append("apps/snake/main.py")
	pinned.append("apps/messages/main.py")
	pinned.append("apps/logger/main.py")
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


ugfx.set_default_font(ugfx.FONT_TITLE)
title = ugfx.Label(3,3,wi-10,45,"EMF Camp 2016",parent=win_header)

ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)

pinned_buttons = []
for i, text in enumerate(file_name):
	x = i % 2
	y = i // 2
	pinned_buttons.append(ugfx.Button(35 + 155 * x, 5 + 40 * y, 120, 35, text, parent=win_quick))

btn_ok = ugfx.Button(10,5,20,20,"A",parent=win_help,shape=ugfx.Button.ELLIPSE)
l_ok = ugfx.Label(40,5,100,20,"Run",parent=win_help)

btn_back = ugfx.Button(100,5,20,20,"B",parent=win_help,shape=ugfx.Button.ELLIPSE)
l_back = ugfx.Label(130,5,100,20,"Back",parent=win_help)

btn_menu = ugfx.Button(200,5,20,20,"M",parent=win_help,shape=ugfx.Button.ROUNDED)
l_back = ugfx.Label(230,5,100,20,"Menu",parent=win_help)

sty = dialogs.default_style_badge

win_header.show()
win_quick.show()
win_help.show()

buttons.init()
cursor = {"x": 0, "y": 0}
last_cursor = cursor.copy()
_draw_cursor(0, 0, sty.background(), win_quick)

app_to_load = "home"

torun = "";

firstrun = database_get("quicklaunch_firstrun", 0)
if not firstrun:

	dialogs.notice("""This screen displays the most commonly used apps.
Apps pinned here can also interact with the name screen.
To view all apps, pin and un-pin, select 'View All'
	""", title="TiLDA - Quick Launch", close_text="Close", width = 213, height = 120)
database_set("quicklaunch_firstrun", 1)

while True:
	pyb.wfi()

	if buttons.is_triggered("JOY_UP"):
		cursor["y"] = max(0, cursor["y"] - 1)
	if buttons.is_triggered("JOY_DOWN"):
		cursor["y"] = min(3, cursor["y"] + 1)
	if buttons.is_triggered("JOY_RIGHT"):
		cursor["x"] = 1
	if buttons.is_triggered("JOY_LEFT"):
		cursor["x"] = 0

	if cursor["x"] != last_cursor["x"] or cursor["y"] != last_cursor["y"]: # Has the cursor moved?
		_draw_cursor(last_cursor["x"], last_cursor["y"], ugfx.WHITE, win_quick)
		_draw_cursor(cursor["x"], cursor["y"], sty.background(), win_quick)
		last_cursor = cursor.copy()

	if buttons.is_triggered("BTN_B"):
		break;

	#if buttons.is_triggered("BTN_MENU"):
	#	open unpin dialog
	#	break;

	if buttons.is_triggered("BTN_A"):
		torun = file_list[cursor["x"] + cursor["y"] * 2]
		print(torun)
		if len(torun) > 3:
			if torun.endswith(".py"):
				break

buttons.disable_all_interrupt()

win_header.hide()
win_quick.hide()
win_help.hide()
for b in pinned_buttons:
	b.destroy()
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
	gc.collect()
	try:
		mod = __import__(torun[:-3])
		if "main" in dir(mod):
			mod.main()
	except Exception as e:
		s = uio.StringIO()
		sys.print_exception(e, s)
		u=pyb.USB_VCP()
		if u.isconnected():
			raise(e)
		else:
			ugfx.clear()
			ugfx.set_default_font(ugfx.FONT_SMALL)
			w=ugfx.Container(0,0,ugfx.width(),ugfx.height())
			l=ugfx.Label(0,0,ugfx.width(),ugfx.height(),s.getvalue(),parent=w)
			w.show()
			while True:
				pyb.wfi()
				if (buttons.is_triggered("BTN_B")) or (buttons.is_triggered("BTN_B")) or (buttons.is_triggered("BTN_MENU")):
					break
			#dialogs.notice(s.getvalue(), width=wi-10, height=hi-10)
	onboard.semihard_reset()
	#ugfx.area(0,0,ugfx.width(),ugfx.height(),0)

	#deinit ugfx here
	#could hard reset here too

#	execfile("apps/%s/main.py" % (app_to_load))
