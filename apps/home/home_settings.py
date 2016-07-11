import ugfx
import pyb
import buttons

wi = ugfx.width()
hi = ugfx.height()
buttons.init()

# ToDo: Move typing logic into a dialog or some other lib

win_header = ugfx.Container(0,0,wi,30)
win_main= ugfx.Container(0,33,int(wi*2/3),int(hi/2)-33)
win_help= ugfx.Container(int(wi*2/3),33,int(wi*1/3),int(hi/2)-33)
win_key = ugfx.Container(0,int(hi/2),wi-2,int(hi/2))

ugfx.set_default_font("D*")
title = ugfx.Label(3,3,wi-10,29,"Change name",win_header)

ugfx.set_default_font("c*")

btn_ok = ugfx.Button(10,win_help.height()-25,20,20,"A",win_help)
l_ok = ugfx.Label(35,win_help.height()-25,100,20,"Save",win_help)

btn_back = ugfx.Button(10,win_help.height()-50,20,20,"B",win_help)
l_back = ugfx.Label(35,win_help.height()-50,100,20,"Move",win_help)

btn_menu = ugfx.Button(10,win_help.height()-75,20,20,"M",win_help)
l_menu = ugfx.Label(35,win_help.height()-75,100,20,"Quit",win_help)


kb = ugfx.Keyboard(0,0,wi,int(hi/2),win_key)
kb.attach_input(ugfx.JOY_UP,0)
kb.attach_input(ugfx.JOY_DOWN,1)
kb.attach_input(ugfx.JOY_RIGHT,2)
kb.attach_input(ugfx.JOY_LEFT,3)
kb.attach_input(ugfx.JOY_CENTER,4)

tim = pyb.Timer(3)
tim.init(freq=60)
tim.callback(lambda t:ugfx.poll())

win_header.show()
win_main.show()
win_key.show()
win_help.show()

while not buttons.is_triggered("BTN_MENU"):
	pyb.wfi()

btn_ok.destroy()
l_ok.destroy()
btn_back.destroy()
l_back.destroy()
btn_menu.destroy()
l_menu.destroy()
win_help.destroy()
win_key.destroy()
win_header.destroy()
win_main.destroy()
kb.destroy()

pyb.hard_reset()
