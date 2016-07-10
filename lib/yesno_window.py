import ugfx
import badge
import pyb

def show_yesno_window(yes_text, no_text,question):
	wi = ugfx.width()
	hi = ugfx.height()
	win = ugfx.Container(int(wi/6),int(hi/4),int(wi*4/6),int(hi/2))
	
	wi = win.width()
	hi = win.height()
	btnyes = ugfx.Button(int(wi/12),int(hi*3/5),int(wi/3),int(hi/5),"A: " + yes_text,win)
	btnno = ugfx.Button(int(wi/2 + wi/12),int(hi*3/5),int(wi/3),int(hi/5),"B: " + no_text,win)
	label = ugfx.Label(int(wi/10),int(hi/10),int(wi*4/5),int(hi*2/5),question,win)
	
	btnyes.attach_input(ugfx.BTN_A,0)
	btnno.attach_input(ugfx.BTN_B,0)
	
	win.show()
	
	b = badge.Badge()
	b.init_pins()
	
	keepgoing = 1
	
	press_a = 0
	press_b = 0
	
	
	
	while keepgoing:
		pyb.wfi()
		if b.is_pressed("BTN_A"):
			press_a = 1
			pyb.delay(10)
		elif press_a:
			keepgoing = 0;
			re = 1
		
		if b.is_pressed("BTN_B"):
			press_b = 1
			pyb.delay(10)
		elif press_b:
			keepgoing = 0;
			re = 0
			
	win.hide()
	
	win.destroy()
	btnyes.destroy()
	btnno.destroy()
	label.destroy()
	
	return re
	