### Author: EMF Badge team
### Description: Change WiFi settings
### Category: Settings
### License: MIT
### Appname : Wifi

import pyb
import buttons
from dialogs import *
from database import *

width = ugfx.width()
height = ugfx.height()
buttons.init()


# Create visual elements
win_header = ugfx.Container(0,0,width,30)
win_main = ugfx.Container(0,33,width,height-33)

components = [win_header, win_main]
ugfx.set_default_font("D*")
components.append(ugfx.Label(3,3,width-10,29,"Wifi Settings",parent=win_header))
ugfx.set_default_font("c*")
components.append(ugfx.Label(40,10,75,25,"Name:",parent=win_main))
components.append(ugfx.Label(40,35,75,25,"Password:",parent=win_main))
lname = ugfx.Label(115,10,100,25,"BadgeNet",parent=win_main)
lpwd = ugfx.Label(115,35,100,25,"letmein",parent=win_main)
components.append(lname)
components.append(lpwd)
ckhide = ugfx.Checkbox(250,35,100,25,"Hide",parent=win_main)
components.append(ckhide)


win_main.show()
win_header.show()

#options = ugfx.List(3,3,win_files.width()-6,win_files.height()-6,parent=win_files)
#components.append(options)
#components.append(ugfx.Button(10,win_preview.height()-25,20,20,"A",parent=win_preview))
#components.append(ugfx.Label(35,win_preview.height()-25,50,20,"Run",parent=win_preview))
#components.append(ugfx.Button(80,win_preview.height()-25,20,20,"B",parent=win_preview))
#components.append(ugfx.Label(105,win_preview.height()-25,100,20,"Back",parent=win_preview))
#components.append(ugfx.Button(10,win_preview.height()-50,20,20,"M",parent=win_preview))
#components.append(ugfx.Label(35,win_preview.height()-50,100,20,"Pin/Unpin",parent=win_preview))
#author = ugfx.Label(1,win_preview.height()-78,win_preview.width()-3,20,"by: ",parent=win_preview)
#desc = ugfx.Label(3,1,win_preview.width()-10,win_preview.height()-83,"Cool app/10",parent=win_preview)
#components.append(author)
#components.append(desc)

timer = pyb.Timer(3)
timer.init(freq=60)
timer.callback(lambda t:ugfx.poll())

try:
	ap = database_get("wifi-ap", "")
	pwd = database_get("wifi-pwd", "")
	
	while True:
	
		if buttons.is_triggered("BTN_B"):
			break

	#name_new = prompt_text("Enter your name", default=name, init_text = name, true_text="OK", false_text="Back", width = 310, height = 220)

	#database_set("display-name", name_new)

finally:
	timer.deinit()

	for component in components:
		component.destroy()