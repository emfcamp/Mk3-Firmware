### Author: EMF Badge team
### Description: Main app
### Category: Other
### License: MIT
### Appname: Home
### Built-in: hide
import ugfx
import pyb
import os
from database import *
from filesystem import *
import buttons
import gc
import stm
import apps.home.draw_name
import wifi


def draw_battery(back_colour,percent, win_bv):
	ugfx.set_default_font("c*")	
	x=3
	y=3
	win_bv.area(x+35,y,40,24,back_colour)
	if percent <= 120:
		win_bv.text(x+35,y,str(int(min(percent,100))),back_colour^0xFFFF)	
	y += 2
	win_bv.area(x,y,30,11,back_colour^0xFFFF)
	win_bv.area(x+30,y+3,3,5,back_colour^0xFFFF)
	
	if percent > 120:
		win_bv.area(x+2,y+2,26,7,ugfx.YELLOW)
	elif percent > 2:
		win_bv.area(x+2,y+2,26,7,back_colour)
		win_bv.area(x+2,y+2,int(min(percent,100)*26/100),7,back_colour^0xFFFF)
	else:
		win_bv.area(x+2,y+2,26,7,ugfx.RED)
	
def draw_wifi(back_colour, rssi, connected, connecting, win_wifi):
	
	outline = [[0,20],[25,20],[25,0]]
	#inline =  [[3,17],[17,17],[17,3]]
	
	#win_wifi.fill_polygon(0, 0, outline, back_colour^0xFFFF)

	if connected:
		win_wifi.fill_polygon(0, 0, outline, ugfx.GREEN)
	elif connecting:
		win_wifi.fill_polygon(0, 0, outline, ugfx.YELLOW)
	else:
		win_wifi.fill_polygon(0, 0, outline, ugfx.RED)

tick = 1
pretick = 0
	
def tick_inc(t):
	global pretick
	pretick += 1
	ugfx.poll()
	
def backlight_adjust():
	l = pyb.ADC(16).read()
	if (l > 90):
		ugfx.backlight(100)
	elif (l > 20):
		ugfx.backlight(70)
	else:
		ugfx.backlight(30)

def get_battery_voltage(adc_obj, ref_obj):
	vin = adc_obj.read()
	ref_reading = ref_obj.read()
	factory_reading = stm.mem16[0x1FFF75AA]
	reference_voltage = factory_reading/4095*3
#	print (str(reference_voltage) + "  " + str(factory_reading) + " " + str(ref_reading))
	supply_voltage = 4095/ref_reading*reference_voltage 
	return 2 * vin / 4095 * supply_voltage
	
def get_home_screen_background_apps():
	pinned = database_get("pinned", [])
	out = []
	for f in pinned:
		if f.endswith("/main.py"):
			fe = f[:-7] + "external.py"
			if is_file(fe):
				out.append(fe)

	return out

def low_power():
	ugfx.backlight(5)

#needs looking at
def get_temperature(adc_obj, ref_obj):
	tval = adc_obj.read()
	ref_reading = ref_obj.read()
	factory_reading = stm.mem16[0x1FFF75AA]
	reference_voltage = factory_reading/4095*3
	supply_voltage = 4095/ref_reading*reference_voltage 
	adc30_3v = stm.mem16[0x1FFF75A8]
	adc110_3v = stm.mem16[0x1FFF75CA]
	grad = (adc110_3v - adc30_3v)/(110-30)
	tval_3v = tval/3*supply_voltage
	diff = (adc30_3v - tval_3v)/grad
	return 30 - diff
	
ugfx.init()

if not stm.mem8[0x40002850] == 0x9C:
	splashes = ["splash1.bmp"]
	for s in splashes:
		ugfx.display_image(0,0,s)
		delay = 5000
		buttons.init()
		while delay:
			delay -= 1
			if buttons.is_triggered("BTN_MENU"):
				break;
			if buttons.is_triggered("BTN_A"):
				break;
			if buttons.is_triggered("BTN_B"):
				break;
			if buttons.is_triggered("JOY_CENTER"):
				break;
			pyb.delay(1)

ugfx.init()
stm.mem8[0x40002850] = 0
sty = ugfx.Style()
sty.set_enabled([ugfx.WHITE, ugfx.html_color(0x3C0246), ugfx.GREY, ugfx.RED])
sty.set_background(ugfx.html_color(0x3C0246))
ugfx.set_default_style(sty)


neo=pyb.Neopix(pyb.Pin("PB13"))
neo.display(0x050505)

while True:
#	ugfx.init()
	
	ugfx.area(0,0,320,240,ugfx.html_color(0x3C0246))
	
	win_bv = ugfx.Container(0,0,80,25)
	win_wifi = ugfx.Container(82,0,60,25)
	win_name = ugfx.Container(0,25,320,240-25-60)
	win_text = ugfx.Container(0,240-60,320,60)

	
	obj_name = apps.home.draw_name.draw(0,25,win_name)

	buttons.init()
	
	gc.collect()
	ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
	l_text = ugfx.List(0,0,250,win_text.height(),parent=win_text)
	
	win_bv.show()
	win_text.show()
	win_wifi.show()	
	
	adc_obj = pyb.ADC(pyb.Pin("ADC_UNREG"))
	ref_obj = pyb.ADC(0)
	temp_obj = pyb.ADC(17)

	
	min_ctr = 28
	
#	timerb = pyb.Timer(3)
#	timerb.init(freq=1)
#	timerb.callback(tick_inc)
	
	timer = pyb.Timer(3)
	timer.init(freq=50)
	timer.callback(tick_inc) #lambda t:ugfx.poll())
	
	
	ext_list = get_home_screen_background_apps()
	ext_import = []
	per_freq=[];
	for e in ext_list:
		ext_import.append(__import__(e[:-3]))
		try:
			per_freq.append(ext_import[-1].update_rate)
		except AttributeError:
			per_freq.append(120)
			
	icons = []
	x = 150
	for e in ext_list:
		icons.append(ugfx.Container(x,0,25,25))
		x += 27
			
	per_time_since = [200]*len(ext_import)
	
	backlight_adjust()
	
	inactivity = 0
	
	
	## start connecting to wifi in the background
	wifi_timeout = 60 #seconds
	wifi_reconnect_timeout = 0
	try:
		wifi.connect(wait = False)
	except OSError:
		Print("Creating default wifi settings file")
		wifi.create_default_config()
	
	while True:
		pyb.wfi()
		
		if (pretick >= 50):
			pretick = 0 
			tick += 1
		
		#if wifi still needs poking
		if (wifi_timeout > 0):
			if wifi.nic().is_connected():
				wifi_timeout = 0
				#wifi is connected, but if becomes disconnected, reconnect after 10sec
				wifi_reconnect_timeout = 10
			else:
				wifi.nic().update()

		
		if tick >= 1:
			tick = 0
			if (wifi_timeout > 0):
				wifi_timeout -= 1;
			
			#if wifi timeout has occured and wifi isnt connected in time
			if (wifi_timeout == 0) and not (wifi.nic().is_connected()):
				print("Giving up on Wifi connect")
				wifi_timeout = -1
				wifi.nic().disconnect()  #give up
				wifi_reconnect_timeout = 60 #try again in 60sec
			
			wifi_connect = wifi.nic().is_connected()
			
			#if not connected, see if we should try again
			if not wifi_connect:
				if wifi_reconnect_timeout>0:
					wifi_reconnect_timeout -= 1
					if wifi_reconnect_timeout == 0:
							wifi_timeout = 60 #seconds
							wifi.connect(wait = False)

			draw_wifi(ugfx.html_color(0x3C0246),0, wifi_connect,wifi_timeout>0,win_wifi)
			
			
			v = get_battery_voltage(adc_obj,ref_obj)
			#t = get_temperature(temp_obj,ref_obj)
			#print(t)
			battery_percent = int((v-3.7)/(4.15-3.7)*100)
			draw_battery(ugfx.html_color(0x3C0246),battery_percent,win_bv)
			
			min_ctr += 1
			inactivity += 1
			
			if battery_percent > 120:  #if charger plugged in
				ugfx.backlight(100)
			elif inactivity > 120:
				low_power()
			else:
				backlight_adjust()
			
			
			# dont run periodic tasks if wifi is pending
			if (min_ctr >= 30) and (wifi_timeout <= 0):							
				for i in range(0, len(ext_import)):
					per_time_since[i] += min_ctr
					if per_time_since[i] >= per_freq[i]:
						per_time_since[i] = 0				
						e = ext_import[i]					
						if "periodic_home" in dir(e):
							text = e.periodic_home(icons[i])
							if len(text) > 0:								
								if (l_text.count() > 10):
									l_text.remove_item(0)
								l_text.add_item(text)
								if l_text.selected_index() >= (l_text.count()-2):
									l_text.selected_index(l_text.count()-1)
				min_ctr = 0	

		if buttons.is_triggered("BTN_MENU"):
			break
		if buttons.is_triggered("BTN_A"):
			inactivity = 0
			tick = 1
		if buttons.is_triggered("BTN_B"):
			inactivity = 0
			tick = 1
			
		#if activity:
		#	inactivity = 0

	for i in icons:
		i.destroy()
	win_bv.destroy()
	win_name.destroy()
	win_text.destroy()
	apps.home.draw_name.draw_destroy(obj_name)
	win_name.destroy()
	l_text.destroy()
	#timerb.deinit()
	timer.deinit()
	ugfx.backlight(100)
	
	#if we havnt connected yet then give up since the periodic function wont be poked
	if  not (wifi.nic().is_connected()):
		wifi.nic().disconnect()
		
	## ToDo: Maybe boot should always chdir to the app folder?
	execfile("apps/home/quick_launch.py")
	
