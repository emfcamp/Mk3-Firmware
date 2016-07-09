import ugfx
import badge
import pyb

def show_notice_window(size_x,size_y,text):
	wi = ugfx.width()
	hi = ugfx.height()
	win = ugfx.Container(int((wi-size_x)/2),int((hi-size_y)/2),size_x,size_y)
	
	l = ugfx.Label(0,0,size_x,size_y,text,win)
	
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
		
		if b.is_pressed("BTN_B"):
			press_b = 1
			pyb.delay(10)
		elif press_b:
			keepgoing = 0;
			
	win.hide()
	
	win.destroy()
	l.destroy()

	