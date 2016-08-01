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
import gc
from imu import IMU
import pyb
import onboard


def draw_battery(back_colour,percent, win_bv):
	percent = max(0,percent)
	ugfx.set_default_font("c*")
	main_c = ugfx.WHITE #back_colour^0xFFFF
	x=3
	y=3
	win_bv.area(x+35,y,40,24,back_colour)
	if percent <= 120:
		win_bv.text(x+35,y,str(int(min(percent,100))),main_c)	
	y += 2
	win_bv.area(x,y,30,11,main_c)
	win_bv.area(x+30,y+3,3,5,main_c)
	
	if percent > 120:
		win_bv.area(x+2,y+2,26,7,ugfx.YELLOW)
	elif percent > 2:
		win_bv.area(x+2,y+2,26,7,back_colour)
		win_bv.area(x+2,y+2,int(min(percent,100)*26/100),7,main_c)
	else:
		win_bv.area(x+2,y+2,26,7,ugfx.RED)
	
def draw_wifi(back_colour, rssi, connected, connecting, win_wifi):
	
	outline = [[0,20],[25,20],[25,0]]
	#inline =  [[3,17],[17,17],[17,3]]
	
	#win_wifi.fill_polygon(0, 0, outline, back_colour^0xFFFF)

	if connected:
		win_wifi.fill_polygon(0, 0, outline, ugfx.WHITE)
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
	if ugfx.backlight() == 0:
		ugfx.power_mode(ugfx.POWER_ON)
	l = pyb.ADC(16).read()
	if (l > 90):
		ugfx.backlight(100)
	elif (l > 20):
		ugfx.backlight(70)
	else:
		ugfx.backlight(30)

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
	ugfx.backlight(0)
	ugfx.power_mode(ugfx.POWER_OFF)

	
ugfx.init()
imu=IMU()
ival = imu.get_acceleration()
if ival['y'] < 0:
	ugfx.orientation(0)
else:
	ugfx.orientation(180)


buttons.init()
if not onboard.is_splash_hidden():
	splashes = ["splash1.bmp"]
	for s in splashes:
		ugfx.display_image(0,0,s)
		delay = 5000		
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


onboard.hide_splash_on_next_boot(False)
sty = ugfx.Style()
# set_enabled([text_colour, edge_colour, fill_colour, progress_colour])
sty.set_enabled([ugfx.WHITE, ugfx.html_color(0x3C0246), ugfx.GREY, ugfx.RED])
sty.set_background(ugfx.html_color(0x3C0246))
ugfx.set_default_style(sty)

sty_tb = ugfx.Style(sty)
sty_tb.set_enabled([ugfx.WHITE, ugfx.html_color(0xA66FB0), ugfx.html_color(0x5e5e5e), ugfx.RED])
sty_tb.set_background(ugfx.html_color(0xA66FB0))

orientation = ugfx.orientation()


while True:
#	ugfx.init()
	
	ugfx.area(0,0,320,240,sty_tb.background())
	
	ugfx.set_default_font(ugfx.FONT_MEDIUM)
	win_bv = ugfx.Container(0,0,80,25, style=sty_tb)
	win_wifi = ugfx.Container(82,0,60,25, style=sty_tb)
	win_name = ugfx.Container(0,25,320,240-25-60, style=sty)
	win_text = ugfx.Container(0,240-60,320,60, style=sty_tb)

	windows = [win_bv, win_wifi, win_text]
	
	obj_name = apps.home.draw_name.draw(0,25,win_name)

	buttons.init()
	
	gc.collect()
	ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
	l_text = ugfx.List(0,0,250,win_text.height(),parent=win_text)
	
	win_bv.show()
	win_text.show()
	win_wifi.show()	
	
	min_ctr = 28
	
	timer = pyb.Timer(3)
	timer.init(freq=50)
	timer.callback(tick_inc)	
	
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
		print("Creating default wifi settings file")
		wifi.create_default_config()
	
	while True:
		pyb.wfi()
		
		if (pretick >= 50):
			pretick = 0 
			tick += 1
		
		#if wifi still needs poking
		if (wifi_timeout > 0):
			if wifi.nic().is_connected():
				wifi_timeout = -1
				#wifi is connected, but if becomes disconnected, reconnect after 10sec
				wifi_reconnect_timeout = 10
			else:
				wifi.nic().update()

		
		if tick >= 1:
			tick = 0
			if (wifi_timeout > 0):
				wifi_timeout -= 1;
				
				
			# change screen orientation
			ival = imu.get_acceleration()
			if ival['y'] < -0.6:
				if orientation != 0:
					ugfx.orientation(0)
			elif ival['y'] > 0.6:
				if orientation != 180:
					ugfx.orientation(180)
			if orientation != ugfx.orientation():
				inactivity = 0
				ugfx.area(0,0,320,240,sty_tb.background())
				orientation = ugfx.orientation()
				for w in windows:
					w.hide(); w.show()
				apps.home.draw_name.draw(0,25,win_name)

			
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

			draw_wifi(sty_tb.background(),0, wifi_connect,wifi_timeout>0,win_wifi)
			
			
			battery_percent = onboard.get_battery_percentage()
			draw_battery(sty_tb.background(),battery_percent,win_bv)
			
			min_ctr += 1
			inactivity += 1
			
			if battery_percent > 120:  #if charger plugged in
				if ugfx.backlight() == 0:
					ugfx.power_mode(ugfx.POWER_ON)
				ugfx.backlight(100)
			elif inactivity > 10:
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
	for w in windows:
		w.destroy()
	apps.home.draw_name.draw_destroy(obj_name)
	win_name.destroy()
	l_text.destroy()
	#timerb.deinit()
	timer.deinit()
	if ugfx.backlight() == 0:
		ugfx.power_mode(ugfx.POWER_ON)
	ugfx.backlight(100)
	ugfx.orientation(180)
	
	#if we havnt connected yet then give up since the periodic function wont be poked
	if wifi_timeout >= 0: # not (wifi.nic().is_connected()):
		wifi.nic().disconnect()
		
	gc.collect()
		
	## ToDo: Maybe boot should always chdir to the app folder?
	execfile("apps/home/quick_launch.py")
	
