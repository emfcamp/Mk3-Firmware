import ugfx
import os
import pyb
import buttons
import dialogs
from database import *
from filesystem import *

width = ugfx.width()
height = ugfx.height()
buttons.init()

# Create visual elements
win_header = ugfx.Container(0,0,width,30)
win_files = ugfx.Container(0,33,int(width/2),height-33)
win_preview = ugfx.Container(int(width/2)+2,33,int(width/2)-2,height-33)
components = [win_header, win_files, win_preview]
ugfx.set_default_font("D*")
components.append(ugfx.Label(3,3,width-10,29,"Choose App",win_header))
ugfx.set_default_font("c*")
options = ugfx.List(3,3,win_files.width()-6,win_files.height()-6,parent=win_files)
components.append(options)
components.append(ugfx.Button(10,win_preview.height()-25,20,20,"A",win_preview))
components.append(ugfx.Label(35,win_preview.height()-25,100,20,"Run",win_preview))
components.append(ugfx.Button(10,win_preview.height()-50,20,20,"B",win_preview))
components.append(ugfx.Label(35,win_preview.height()-50,100,20,"Back",win_preview))
components.append(ugfx.Button(10,win_preview.height()-75,20,20,"M",win_preview))
components.append(ugfx.Label(35,win_preview.height()-75,100,20,"Pin/Unpin",win_preview))

# Timer is needed to redraw everything while the rest is sleeping
timer = pyb.Timer(3)
timer.init(freq=60)
timer.callback(lambda t:ugfx.poll())

def update_options(options, apps, pinned):
	while options.count():
		options.remove_item(0)
	for app in apps:
		if app in pinned:
			options.add_item("*" + app)
		else:
			options.add_item(app)

try:
	win_header.show()
	win_files.show()
	win_preview.show()

	pinned = database_get("pinned", [])
	apps = []

	if is_dir("apps"):
		for app in os.listdir("apps"):
			path = "apps/" + app
			if is_dir(path) and is_file(path + "/main.py"):
				apps.append(app)

	update_options(options, apps, pinned)

	while True:
		pyb.wfi()
		if buttons.is_triggered("BTN_MENU"):
			app = apps[options.get_selected_index()]
			if app in pinned:
				pinned.remove(app)
			else:
				pinned.append(app)
			update_options(options, apps, pinned)
			database_set("pinned", pinned)

		if buttons.is_triggered("BTN_B"):
			break

		if buttons.is_triggered("BTN_A"):
			# ToDo: Do something to go to the app
			break

finally:
	for component in components:
		component.destroy()

	timer.deinit()
