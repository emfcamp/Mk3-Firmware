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
from app import *

ugfx.init()
ugfx.set_default_style(dialogs.default_style_badge)
ugfx.clear(ugfx.html_color(dialogs.default_style_badge.background()))

def _draw_cursor (x, y, color, win_quick):
	win_quick.fill_polygon(10 + x * 155, 15 + y * 40, [[0,0],[20,7],[0,14],[4,7]], color)

def quick_launch_screen():
	wi = ugfx.width()
	hi = ugfx.height()

	win_header = ugfx.Container(0,0,wi,30)
	win_quick = ugfx.Container(0,33,wi,hi-33-33)
	win_help = ugfx.Container(0,hi-30,wi,30)

	DEFAULT_APPS = ["app_library", "sponsors", "changename"]
	with Database() as db:
		pinned = [App(a) for a in db.get("pinned_apps", DEFAULT_APPS)]
		pinned = [app for app in pinned if app.loadable] # Filter out deleted apps
		pinned = pinned[:7] # Limit to 7
		db.set("pinned_apps", [app.folder_name for app in pinned])

	ugfx.set_default_font(ugfx.FONT_TITLE)
	title = ugfx.Label(3,3,wi-10,45,"EMF Camp 2016",parent=win_header)

	ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)

	pinned_buttons = []
	for i in range(0, 8):
		x = i % 2
		y = i // 2
		button_title = "View all" if i == 7 else ""
		if i < len(pinned):
			button_title = pinned[i].title
		pinned_buttons.append(ugfx.Button(35 + 155 * x, 5 + 40 * y, 120, 35, button_title, parent=win_quick))

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
	_draw_cursor(0, 0, ugfx.RED, win_quick)

	app_to_load = "home"

	if not database_get("quicklaunch_firstrun"):
		dialogs.notice("""This screen displays the most commonly used apps.
Apps pinned here can also interact with the name screen.
To view all apps, pin and un-pin, select 'View All'
		""", title="TiLDA - Quick Launch", close_text="Close")
		database_set("quicklaunch_firstrun", True)

	try:
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
				_draw_cursor(last_cursor["x"], last_cursor["y"], dialogs.default_style_badge.background(), win_quick)
				_draw_cursor(cursor["x"], cursor["y"], ugfx.RED, win_quick)
				last_cursor = cursor.copy()

			if buttons.is_triggered("BTN_B"):
				return None

			#if buttons.is_triggered("BTN_MENU"):
			#	open unpin dialog
			#	break;

			if buttons.is_triggered("BTN_A"):
				index = cursor["x"] + cursor["y"] * 2
				if index == 7:
					return "file_loader"
				if index < len(pinned):
					return pinned[index]
	finally:
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

torun = quick_launch_screen()
if torun:
	print("Running: %s" % torun)
	empty_local_app_cache()
	
	gc.collect()
	pyb.info()
	
	import run_app
	run_app.run_app("apps/home/file_loader" if torun == "file_loader" else torun.main_path[:-3])
	
	#ugfx.area(0,0,ugfx.width(),ugfx.height(),0)

	#deinit ugfx here
	#could hard reset here too

#	execfile("apps/%s/main.py" % (app_to_load))
