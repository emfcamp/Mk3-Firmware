import ugfx
import os
import pyb
import stm
import buttons
import dialogs
from database import *
from filesystem import *

width = ugfx.width()
height = ugfx.height()
buttons.init()
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
btnr = ugfx.Button(5,3,20,20,"<",parent=win_files)
btnl = ugfx.Button(win_files.width()-7-20,3,20,20,">",parent=win_files)
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

# Timer is needed to redraw everything while the rest is sleeping
timer = pyb.Timer(3)
timer.init(freq=60)
timer.callback(lambda t:ugfx.poll())

app_to_load = ""

catergories = ["Built-in", "Examples", "Settings", "Games", "Comms", "Other", "All"]
c_ptr = 0

def update_options(options, apps, pinned, cat):
#	options.selected_index(0)
	options.disable_draw()
	cat = cat.lower()
	out = []
	while options.count():
		options.remove_item(0)
	for app in apps:
		att_name = get_app_attribute(app,"Appname")
		app_cat = get_app_attribute(app,"Category").lower()
		
		#handle unspecified
		if len(app_cat) == 0:
			app_cat = "other"
			
		if app.startswith("examples/"):
			app_cat = "examples"
			
		#handle the 'built-in' category
		b_in = get_app_attribute(app,"built-in").lower()
		
		#see if we should show this app
		if (app_cat == cat) | (cat == "all") | ((b_in == "yes") & (cat == "built-in")):
			if not b_in == "hide":	#enables the hiding of the home screen to stop it calling itself
				if len(att_name) == 0:
					att_name = get_app_foldername(app)
				if app in pinned:
					options.add_item("*" + att_name)
				else:
					options.add_item(att_name)
				out.append(app)
		
		
	options.enable_draw()
	return out

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
				apps_path.append(path + "/main.py")
	if is_dir("examples"):
		for app in os.listdir("examples"):
			path = "examples/" + app
			if is_file(path) and path.endswith(".py"):
				apps_path.append(path)

	displayed_apps = update_options(options, apps_path, pinned, catergories[c_ptr])

	index_prev = -1;
	
	while True:
		pyb.wfi()
		
		if index_prev != options.selected_index():
			if options.selected_index() < len(displayed_apps):
				author.text("by: " + get_app_attribute(displayed_apps[options.selected_index()],"author"))
				desc.text(get_app_attribute(displayed_apps[options.selected_index()],"description"))
			index_prev = options.selected_index()
		
		if buttons.is_triggered("JOY_LEFT"):
			if c_ptr > 0:
				c_ptr -= 1
				l_cat.text(catergories[c_ptr])
				displayed_apps = update_options(options, apps_path, pinned, catergories[c_ptr])
				index_prev = -1
		
		if buttons.is_triggered("JOY_RIGHT"):
			if c_ptr < len(catergories)-1:
				c_ptr += 1
				l_cat.text(catergories[c_ptr])
				displayed_apps = update_options(options, apps_path, pinned, catergories[c_ptr])
				index_prev = -1
		
		if buttons.is_triggered("BTN_MENU"):
			app_path = displayed_apps[options.selected_index()]
			if app_path in pinned:
				pinned.remove(app_path)
			else:
				pinned.append(app_path)
			update_options(options, apps_path, pinned, catergories[c_ptr])
			database_set("pinned", pinned)

		if buttons.is_triggered("BTN_B"):
			break

		if buttons.is_triggered("BTN_A"):
			# ToDo: Do something to go to the app
			app_to_load = displayed_apps[options.selected_index()] #"test_app1"
			break

finally:
	for component in components:
		component.destroy()

	timer.deinit()

if len(app_to_load) > 0:
	try:
		buttons.enable_menu_reset()
		
		print("Loading: " + app_to_load)
		mod = __import__(app_to_load[:-3])
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
			w=ugfx.Container(0,0,ugfx.width(),ugfx.height())
			l=ugfx.Label(0,0,ugfx.width(),ugfx.height(),s.getvalue(),parent=w)
			w.show()
			while True:
				pyb.wfi()
				if (buttons.is_triggered("BTN_B")) or (buttons.is_triggered("BTN_B")) or (buttons.is_triggered("BTN_MENU")):
					break;
			#str=s.getvalue().split("\n")
			#if len(str)>=4:
			#out = "\n".join(str[4:])			
			#dialogs.notice(out, width=wi-10, height=hi-10)
	stm.mem8[0x40002850] = 0x9C
	pyb.hard_reset()
	
	#deinit ugfx here
	#could hard reset here too
