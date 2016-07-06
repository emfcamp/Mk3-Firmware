import ugfx
import os

#options.destroy()
#btn_ok.destroy()
#btn_menu.destroy()

ugfx.init()

ugfx.set_default_font("D*")

ugfx.text(40, 0, "EMF BADGE 2016", ugfx.PURPLE)

ugfx.set_default_font("C*")

options = ugfx.List(0,0,160,150)
btn_ok = ugfx.Button(200,50,70,30,"A: Run")
btn_menu = ugfx.Button(200,90,70,30,"M: Menu")

files = os.listdir()

for f in files:
	options.add_item(f)

btn_menu.attach_input(ugfx.BTN_MENU)
btn_ok.attach_input(ugfx.BTN_A)
