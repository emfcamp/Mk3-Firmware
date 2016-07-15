import ugfx
import pyb
import buttons

ugfx.init()
wi = ugfx.width()
hi = ugfx.height()
buttons.init()

# ToDo: Move typing logic into a dialog or some other lib
win_header = ugfx.Container(0,0,wi,30)
win_help= ugfx.Container(int(wi*2/3),33,int(wi*1/3),int(hi/2)-33)
win_key = ugfx.Container(0,int(hi/2),wi,int(hi/2))

ugfx.set_default_font("D*")
title = ugfx.Label(3,3,wi-10,29,"Change name",parent=win_header)

ugfx.set_default_font("c*")

btn_ok = ugfx.Button(10,win_help.height()-25,20,20,text="A",parent=win_help, trigger=ugfx.BTN_A)
l_ok = ugfx.Label(35,win_help.height()-25,100,20,"Save",parent=win_help)

btn_back = ugfx.Button(10,win_help.height()-50,20,20,text="B",parent=win_help, trigger=ugfx.BTN_B)
l_back = ugfx.Label(35,win_help.height()-50,100,20,"Move",parent=win_help)

btn_menu = ugfx.Button(10,win_help.height()-75,20,20,text="M",parent=win_help, trigger=ugfx.BTN_MENU)
l_menu = ugfx.Label(35,win_help.height()-75,100,20,"Quit",parent=win_help)

kb = ugfx.Keyboard(0, 0, wi, int(hi/2), parent=win_key)

textbox=ugfx.Textbox(0,33,int(wi*2/3),int(hi/2)-33)

tim = pyb.Timer(3)
tim.init(freq=60)
tim.callback(lambda t:ugfx.poll())

win_header.show()
win_key.show()
win_help.show()

while not buttons.is_triggered("BTN_MENU"):
    if buttons.is_triggered("BTN_A"):
        print("A")
    if buttons.is_triggered("BTN_B"):
        print("B")
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
textbox.destroy()
kb.destroy()

pyb.hard_reset()
