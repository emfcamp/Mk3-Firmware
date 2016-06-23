import ugfx
import os

#options.destroy()
#btn_ok.destroy()
#btn_menu.destroy()

ugfx.init()

ugfx.set_default_font("D*")

ugfx.text("EMF BADGE 2016",40,0,ugfx.PURPLE)

ugfx.set_default_font("C*")

options = ugfx.List(10,50,160,200)
btn_ok = ugfx.Button(200,50,70,30,"A: Run")
btn_menu = ugfx.Button(200,90,70,30,"M: Menu")

files = os.listdir()

for f in files:
	options.add_item(f)
	
options.attach_input(ugfx.JOY_UP,0)
options.attach_input(ugfx.JOY_DOWN,1)
btn_menu.attach_input(ugfx.BTN_MENU)
btn_ok.attach_input(ugfx.BTN_A)
