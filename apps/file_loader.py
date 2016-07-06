import ugfx
import os
import pyb
import badge
import yesno_window

def main():
	wi = ugfx.width()
	hi = ugfx.height()
	b = badge.Badge()
	b.init_pins()

	win_header = ugfx.Container(0,0,wi,30)
	win_files = ugfx.Container(0,33,int(wi/2),hi-33)
	win_preview = ugfx.Container(int(wi/2)+2,33,int(wi/2)-2,hi-33)


	ugfx.set_default_font("D*")
	title = ugfx.Label(3,3,wi-10,29,"Choose File",win_header)


	ugfx.set_default_font("c*")
	options = ugfx.List(3,3,win_files.width()-6,win_files.height()-6,parent=win_files)

	btn_ok = ugfx.Button(10,win_preview.height()-25,20,20,"A",win_preview)
	l_ok = ugfx.Label(35,win_preview.height()-25,100,20,"Run",win_preview)

	btn_back = ugfx.Button(10,win_preview.height()-50,20,20,"B",win_preview)
	l_back = ugfx.Label(35,win_preview.height()-50,100,20,"Back",win_preview)

	btn_menu = ugfx.Button(10,win_preview.height()-75,20,20,"M",win_preview)
	l_back = ugfx.Label(35,win_preview.height()-75,100,20,"Pin",win_preview)


	tim = pyb.Timer(3)
	tim.init(freq=60)
	tim.callback(lambda t:ugfx.poll())
	
	win_header.show()
	win_files.show()
	win_preview.show()


	folders = os.listdir("/flash/apps")
	filepaths = []
	for folder in folders:
		try: #is there a better way of doing this in upy?
			appfiles = os.listdir("/flash/apps/" + folder)
			if ((folder+".py") in appfiles):
				options.add_item(folder)
				filepaths.append("apps/" + folder + "/" + folder+".py")
		except:
			2+2
			#ignore and continue
			
	files = os.listdir("/flash/examples")
	for file in files:
		if file.endswith(".py"):
			options.add_item(file[:-3])
			filepaths.append("examples/" + file)

	
	
	#files = os.listdir()

	#for f in files:
	#	if f.endswith(".py"):
	#		options.add_item(f)

	options.attach_input(ugfx.JOY_UP,0)
	options.attach_input(ugfx.JOY_DOWN,1)
	#btn_menu.attach_input(ugfx.BTN_MENU)
	#btn_ok.attach_input(ugfx.BTN_A)

	stay_here = 1;

	while(stay_here):
		pyb.wfi()
		if b.is_pressed("BTN_MENU"):
			try:			
				towrite = filepaths[options.get_selected_index()]
				
				if len(towrite) > 3:
					r = yesno_window.show_yesno_window("Yes","No","Confirm add '"+options.get_selected_text() + "' to quick-launch?")
					if r:
						fhw = open("/flash/pinned.txt",'a')
						fhw.write(towrite + "\r\n")
						fhw.flush()
						fhw.close()
			except:
				print("Error appending file")
			pyb.delay(1500)
		
		if b.is_pressed("BTN_B"):
			stay_here = 0
	
	win_header.destroy()
	win_files.destroy()
	win_preview.destroy()
	title.destroy()
	options.destroy()
	btn_ok.destroy()
	l_ok.destroy()
	btn_back.destroy()
	l_back.destroy()
	btn_menu.destroy()
	l_back.destroy()
	tim.deinit()
		
		
