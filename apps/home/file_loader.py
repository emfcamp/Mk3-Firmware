import ugfx
import os
import pyb
import badge
import yesno_window

def update_list(folder_in, ui_options):	
	filepaths = []
	
	while(ui_options.count()):
		ui_options.remove_item(0)
	
	try:
		f = os.listdir("/flash/"+folder_in)
	except:
		return []
	if folder_in == "examples":	
		for file in f:
			if file.endswith(".py"):
				ui_options.add_item(file[:-3])
				filepaths.append("examples/" + file)
	else:		
		for folder in f:
			try: #is there a better way of doing this in upy?
				appfiles = os.listdir("/flash/"+ folder_in +"/" + folder)
				if (("main.py") in appfiles):
					ui_options.add_item(folder)
					filepaths.append(folder_in + "/" + folder + "/main.py")
			except:
				2+2
				#ignore and continue
			
	return filepaths

def main():
	wi = ugfx.width()
	hi = ugfx.height()
	b = badge.Badge()
	b.init_pins()
	
	top_folders = ["apps","examples","settings"]
	top_folders_ptr = 0

	win_header = ugfx.Container(0,0,wi,30)
	win_files = ugfx.Container(0,33,int(wi/2),hi-33)
	win_preview = ugfx.Container(int(wi/2)+2,33,int(wi/2)-2,hi-33)


	ugfx.set_default_font("D*")
	title = ugfx.Label(3,3,wi-10,29,"Choose File",win_header)


	ugfx.set_default_font("c*")
	options = ugfx.List(0,25,win_files.width(),win_files.height()-25,parent=win_files)

	btn_ok = ugfx.Button(10,win_preview.height()-25,20,20,"A",win_preview)
	l_ok = ugfx.Label(35,win_preview.height()-25,100,20,"Run",win_preview)

	btn_back = ugfx.Button(10,win_preview.height()-50,20,20,"B",win_preview)
	l_back = ugfx.Label(35,win_preview.height()-50,100,20,"Back",win_preview)

	btn_menu = ugfx.Button(10,win_preview.height()-75,20,20,"M",win_preview)
	l_back = ugfx.Label(35,win_preview.height()-75,100,20,"Pin",win_preview)
	
	btn_r = ugfx.Button(3,3,20,20,"<",win_files)
	btn_l = ugfx.Button(win_files.width()-25,3,20,20,">",win_files)
	l_folder = ugfx.Label(25,3,win_files.width()-55,20,"Apps",win_files)


	tim = pyb.Timer(3)
	tim.init(freq=60)
	tim.callback(lambda t:ugfx.poll())
	
	win_header.show()
	win_files.show()
	win_preview.show()

	filepaths = update_list(top_folders[top_folders_ptr],options)
	

	options.attach_input(ugfx.JOY_UP,0)
	options.attach_input(ugfx.JOY_DOWN,1)
	btn_r.attach_input(ugfx.JOY_LEFT,0)
	btn_l.attach_input(ugfx.JOY_RIGHT,0)
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
			
		if b.is_pressed("JOY_LEFT"):
			top_folders_ptr += 1
			if top_folders_ptr >= len(top_folders):
				top_folders_ptr = 0;
			filepaths = update_list(top_folders[top_folders_ptr],options)
			l_folder.text(top_folders[top_folders_ptr])
			while b.is_pressed("JOY_LEFT"):
				pyb.delay(70)
		if b.is_pressed("JOY_RIGHT"):
			top_folders_ptr -= 1
			if top_folders_ptr < 0:
				top_folders_ptr = len(top_folders)-1;
			filepaths = update_list(top_folders[top_folders_ptr],options)
			l_folder.text(top_folders[top_folders_ptr])
			while b.is_pressed("JOY_RIGHT"):
				pyb.delay(70)

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
	btn_r.destroy()
	btn_l.destroy()
	l_folder.destroy()
		
		
