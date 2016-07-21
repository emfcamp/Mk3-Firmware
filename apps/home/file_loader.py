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
components.append(ugfx.Label(3,3,width-10,29,"Choose App",parent=win_header))
ugfx.set_default_font("c*")
options = ugfx.List(3,3,win_files.width()-6,win_files.height()-6,parent=win_files)
components.append(options)
components.append(ugfx.Button(10,win_preview.height()-25,20,20,"A",parent=win_preview))
components.append(ugfx.Label(35,win_preview.height()-25,100,20,"Run",parent=win_preview))
components.append(ugfx.Button(10,win_preview.height()-50,20,20,"B",parent=win_preview))
components.append(ugfx.Label(35,win_preview.height()-50,100,20,"Back",parent=win_preview))
components.append(ugfx.Button(10,win_preview.height()-75,20,20,"M",parent=win_preview))
components.append(ugfx.Label(35,win_preview.height()-75,100,20,"Pin/Unpin",parent=win_preview))

# Timer is needed to redraw everything while the rest is sleeping
timer = pyb.Timer(3)
timer.init(freq=60)
timer.callback(lambda t:ugfx.poll())

app_to_load = ""

def update_options(options, apps, pinned):
	while options.count():
		options.remove_item(0)
	for app in apps:
		if app in pinned:
			options.add_item("*" + get_app_name(app))
		else:
			options.add_item(get_app_name(app))

try:
	win_header.show()
	win_files.show()
	win_preview.show()

	pinned = database_get("pinned", [])
#	apps = []
	apps_path = []

	if is_dir("apps"):
		for app in os.listdir("apps"):
			path = "apps/" + app
			if is_dir(path) and is_file(path + "/main.py"):
#				apps.append(app)
				apps_path.append(path + "/main.py")

	update_options(options, apps_path, pinned)

	while True:
		pyb.wfi()
		if buttons.is_triggered("BTN_MENU"):
			app_path = apps_path[options.get_selected_index()]
			if app_path in pinned:
				pinned.remove(app_path)
			else:
				pinned.append(app_path)
			update_options(options, apps_path, pinned)
			database_set("pinned", pinned)

		if buttons.is_triggered("BTN_B"):
			break

		if buttons.is_triggered("BTN_A"):
			# ToDo: Do something to go to the app
			app_to_load = apps_path[options.get_selected_index()] #"test_app1"
			break

finally:
	for component in components:
		component.destroy()

	timer.deinit()

if len(app_to_load) > 0:
	#try:
	mod = __import__(app_to_load[:-3])
	if "main" in dir(mod):
		mod.main()
	#except Exception as e:
	#	dialogs.notice(str(e), width=wi-20, height=hi-20)
	ugfx.area(0,0,ugfx.width(),ugfx.height(),0)
	#deinit ugfx here
	#could hard reset here too

#	execfile("apps/%s/main.py" % (app_to_load))
print("Leaving file loader")