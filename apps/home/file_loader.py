import ugfx
import os
import pyb
import buttons
import dialogs
from database import *
from filesystem import *
import uio
import sys
import gc
import onboard
from app import *

ugfx.init()
buttons.init()
ugfx.set_default_style(dialogs.default_style_badge)
ugfx.clear(ugfx.html_color(dialogs.default_style_badge.background()))

def update_options(options, category, pinned):
	options.disable_draw()
	apps = get_local_apps(category)
	out = []
	while options.count():
		options.remove_item(0)

	for app in apps:
		if app.get_attribute("built-in") == "hide":
			continue # No need to show the home app

		if app.folder_name in pinned:
			options.add_item("*%s" % app.title)
		else:
			options.add_item(app.title)
		out.append(app)

	options.selected_index(0)
	options.enable_draw()
	return out

def file_loader():
	width = ugfx.width()
	height = ugfx.height()
	buttons.disable_menu_reset()

	# Create visual elements
	win_header = ugfx.Container(0,0,width,30)
	win_files = ugfx.Container(0,33,int(width/2),height-33)
	win_preview = ugfx.Container(int(width/2)+2,33,int(width/2)-2,height-33)
	components = [win_header, win_files, win_preview]
	ugfx.set_default_font(ugfx.FONT_TITLE)
	components.append(ugfx.Label(3,3,width-10,29,"Choose App",parent=win_header))
	ugfx.set_default_font(ugfx.FONT_MEDIUM)
	options = ugfx.List(0,30,win_files.width(),win_files.height()-30,parent=win_files)
	btnl = ugfx.Button(5,3,20,20,"<",parent=win_files)
	btnr = ugfx.Button(win_files.width()-7-20,3,20,20,">",parent=win_files)
	btnr.attach_input(ugfx.JOY_RIGHT,0)
	btnl.attach_input(ugfx.JOY_LEFT,0)
	components.append(options)
	components.append(btnr)
	components.append(btnl)
	ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
	l_cat = ugfx.Label(30,3,100,20,"Built-in",parent=win_files)
	components.append(l_cat)
	components.append(ugfx.Button(10,win_preview.height()-25,20,20,"A",parent=win_preview))
	components.append(ugfx.Label(35,win_preview.height()-25,50,20,"Run",parent=win_preview))
	components.append(ugfx.Button(80,win_preview.height()-25,20,20,"B",parent=win_preview))
	components.append(ugfx.Label(105,win_preview.height()-25,100,20,"Back",parent=win_preview))
	components.append(ugfx.Button(10,win_preview.height()-50,20,20,"M",parent=win_preview))
	components.append(ugfx.Label(35,win_preview.height()-50,100,20,"Pin/Unpin",parent=win_preview))
	ugfx.set_default_font(ugfx.FONT_SMALL)
	author = ugfx.Label(1,win_preview.height()-78,win_preview.width()-3,20,"by: ",parent=win_preview)
	desc = ugfx.Label(3,1,win_preview.width()-10,win_preview.height()-83,"",parent=win_preview,justification=ugfx.Label.LEFTTOP)
	components.append(author)
	components.append(desc)

	app_to_load = None

	pinned = database_get("pinned_apps", [])
	catergories = get_local_app_categories()
	c_ptr = 0

	try:
		win_header.show()
		win_files.show()
		win_preview.show()

		pinned = database_get("pinned_apps", [])
	#	apps = []
		apps_path = []

		if is_dir("apps"):
			for app in os.listdir("apps"):
				path = "apps/" + app
				if is_dir(path) and is_file(path + "/main.py"):
					apps_path.append(path + "/main.py")
		if is_dir("examples"):
			for app in os.listdir("examples"):
				path = "examples/" + app
				if is_file(path) and path.endswith(".py"):
					apps_path.append(path)

		displayed_apps = update_options(options, catergories[c_ptr], pinned)

		index_prev = -1;

		while True:
			pyb.wfi()
			ugfx.poll()

			if index_prev != options.selected_index():
				if options.selected_index() < len(displayed_apps):
					author.text("by: %s" % displayed_apps[options.selected_index()].user)
					desc.text(displayed_apps[options.selected_index()].description)
				index_prev = options.selected_index()

			if buttons.is_triggered("JOY_LEFT"):
				if c_ptr > 0:
					c_ptr -= 1
					btnl.set_focus()
					l_cat.text(catergories[c_ptr])
					displayed_apps = update_options(options, catergories[c_ptr], pinned)
					index_prev = -1

			if buttons.is_triggered("JOY_RIGHT"):
				if c_ptr < len(catergories)-1:
					c_ptr += 1
					btnr.set_focus()
					l_cat.text(catergories[c_ptr])
					displayed_apps = update_options(options, catergories[c_ptr], pinned)
					index_prev = -1

			if buttons.is_triggered("BTN_MENU"):
				app = displayed_apps[options.selected_index()]
				if app.folder_name in pinned:
					pinned.remove(app.folder_name)
				else:
					pinned.append(app.folder_name)
				update_options(options, catergories[c_ptr], pinned)
				database_set("pinned_apps", pinned)

			if buttons.is_triggered("BTN_B"):
				return None

			if buttons.is_triggered("BTN_A"):
				return displayed_apps[options.selected_index()]

	finally:
		for component in components:
			component.destroy()

app_to_load = file_loader()
if app_to_load:
	gc.collect()
	buttons.enable_menu_reset()
	import run_app
	rbr = app_to_load.get_attribute("reboot-before-run")
	if type(rbr) == str and rbr.lower() == "false": 
		run_app.run_app(app_to_load.main_path[:-3])
	run_app.reset_and_run(app_to_load.main_path[:-3])
	
	
