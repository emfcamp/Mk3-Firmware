### Author: EMF Badge team
### Description: Main app
### Category: Other
### License: MIT
### Appname: Home
### Built-in: hide


import ugfx
import pyb
from database import Database
from filesystem import is_file
import buttons
import gc
import apps.home.draw_name
import wifi
from imu import IMU
import onboard
import dialogs
from app import get_local_apps
import sys
import ntp

def draw_battery(back_colour,percent, win_bv):
	percent = max(0,percent)
	ugfx.set_default_font("c*")
	main_c = ugfx.WHITE #back_colour^0xFFFF
	x=3
	y=3
	win_bv.area(x+35,y,40,19,back_colour)
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

	x = int((rssi+100)/14)
	x = min(5,x)
	x = max(1,x)
	y = x*4
	x = x*5

	outline	  = [[0,20],[25,20],[25,0]]
	outline_rssi = [[0,20],[x,20],[x,20-y]]

	#win_wifi.fill_polygon(0, 0, outline, back_colour^0xFFFF)

	if connected:
		win_wifi.fill_polygon(0, 0, outline, ugfx.html_color(0xC4C4C4))
		win_wifi.fill_polygon(0, 0, outline_rssi, ugfx.WHITE)
	elif connecting:
		win_wifi.fill_polygon(0, 0, outline, ugfx.YELLOW)
	else:
		win_wifi.fill_polygon(0, 0, outline, ugfx.RED)


def draw_time(bg_colour, datetime, win_clock):
	win_clock.area(0, 0, win_clock.width(), win_clock.height(), bg_colour)

	digit_width = 9
	right_padding = 5
	time_text = "%02d:%02d" % (datetime[4], datetime[5])
	start_x = win_clock.width() - (digit_width * len(time_text)) - right_padding
	start_y = 5
	win_clock.text(start_x, start_y, time_text, ugfx.WHITE)


next_tick = 0
tick = True

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

# Finds all locally installed apps that have an external.py
def get_external_hook_paths():
	return ["%s/external" % app.folder_path for app in get_local_apps() if is_file("%s/external.py" % app.folder_path)]

def low_power():
	ugfx.backlight(0)
	ugfx.power_mode(ugfx.POWER_OFF)


ugfx.init()
imu=IMU()
neo = pyb.Neopix(pyb.Pin("PB13"))
neo.display(0x04040404)
ledg = pyb.LED(2)
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
		delay = 2000
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

ugfx.set_default_style(dialogs.default_style_badge)

sty_tb = ugfx.Style(dialogs.default_style_badge)
sty_tb.set_enabled([ugfx.WHITE, ugfx.html_color(0xA66FB0), ugfx.html_color(0x5e5e5e), ugfx.RED])
sty_tb.set_background(ugfx.html_color(0xA66FB0))

orientation = ugfx.orientation()

with Database() as db:
	if not db.get("home_firstrun"):
		stats_upload = dialogs.prompt_boolean("""Press menu to see all the available apps and download more.""", title="Welcome to the EMF camp badge!", true_text="A: OK", false_text = None, width = 320, height = 240)
		db.set("home_firstrun", True)
		db.set("stats_upload", stats_upload)

def home_main():
	global orientation, next_tick, tick

	ugfx.area(0,0,320,240,sty_tb.background())

	ugfx.set_default_font(ugfx.FONT_MEDIUM)
	win_bv = ugfx.Container(0,0,80,25, style=sty_tb)
	win_wifi = ugfx.Container(82,0,60,25, style=sty_tb)
	win_name = ugfx.Container(0,25,320,240-25-60, style=dialogs.default_style_badge)
	win_text = ugfx.Container(0,240-60,320,60, style=sty_tb)
	win_clock = ugfx.Container(250, 0, 70, 25, style=sty_tb)

	windows = [win_bv, win_wifi, win_clock, win_text]

	obj_name = apps.home.draw_name.draw(0,25,win_name)

	buttons.init()

	gc.collect()
	ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
	hook_feeback = ugfx.List(0, 0, win_text.width(), win_text.height(), parent=win_text)

	win_bv.show()
	win_text.show()
	win_wifi.show()
	win_clock.show()

	# Create external hooks so other apps can run code in the context of
	# the home screen.
	# To do so an app needs to have an external.py with a tick() function.
	# The tick period will default to 60 sec, unless you define something
	# else via a "period" variable in the module context (use milliseconds)
	# If you set a variable "needs_wifi" in the module context tick() will
	# only be called if wifi is available
	# If you set a variable "needs_icon" in the module context tick() will
	# be called with a reference to a 25x25 pixel ugfx container that you
	# can modify
	external_hooks = []
	icon_x = 150
	for path in get_external_hook_paths():
		try:
			module = __import__(path)
			if not hasattr(module, "tick"):
				raise Exception("%s must have a tick function" % path)

			hook = {
				"name": path[5:-9],
				"tick": module.tick,
				"needs_wifi": hasattr(module, "needs_wifi"),
				"period": module.period if hasattr(module, "period") else 60 * 1000,
				"next_tick_at": 0
			}

			if hasattr(module, "needs_icon"):
				hook["icon"] = ugfx.Container(icon_x, 0, 25, 25)
				icon_x += 27

			external_hooks.append(hook)
		except Exception as e: # Since we dont know what exception we're looking for, we cant do much
			print ("%s while parsing background task %s.  This task will not run! " % (type(e).__name__, path[5:-9]))
			sys.print_exception(e)
			continue # If the module fails to load or dies during the setup, skip it

	backlight_adjust()

	inactivity = 0
	last_rssi = 0

	## start connecting to wifi in the background
	wifi_timeout = 30 #seconds
	wifi_reconnect_timeout = 0
	wifi_did_connect = 0
	try:
		wifi.connect(wait = False, prompt_on_fail = False)
	except OSError:
		print("Connect failed")

	while True:
		pyb.wfi()
		ugfx.poll()

		if (next_tick <= pyb.millis()):
			tick = True
			next_tick = pyb.millis() + 1000

		#if wifi still needs poking
		if (wifi_timeout > 0):
			if wifi.nic().is_connected():
				wifi_timeout = -1
				#wifi is connected, but if becomes disconnected, reconnect after 5 sec
				wifi_reconnect_timeout = 5
			else:
				wifi.nic().update()


		if tick:
			tick = False

			ledg.on()

			if (wifi_timeout > 0):
				wifi_timeout -= 1;

			# change screen orientation
			ival = imu.get_acceleration()
			if ival['y'] < -0.5:
				if orientation != 0:
					ugfx.orientation(0)
			elif ival['y'] > 0.5:
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
				wifi_reconnect_timeout = 30 #try again in 30sec

			wifi_is_connected = wifi.nic().is_connected()

			#if not connected, see if we should try again
			if not wifi_is_connected:
				if wifi_did_connect > 0:
					wifi_did_connect = 0
				if wifi_reconnect_timeout>0:
					wifi_reconnect_timeout -= 1
					if wifi_reconnect_timeout == 0:
						wifi_timeout = 60 #seconds
						wifi.connect(wait = False)
			else:
				# If we've just connected, set NTP time
				if wifi_did_connect == 0:
					wifi_did_connect = 1
					ntp.set_NTP_time()

			ledg.on()

			# display the wifi logo
			rssi = wifi.nic().get_rssi()
			if rssi == 0:
				rssi = last_rssi
			else:
				last_rssi = rssi

			time = pyb.RTC().datetime()
			if time[0] >= 2016:
				draw_time(sty_tb.background(), pyb.RTC().datetime(), win_clock)

			draw_wifi(sty_tb.background(),rssi, wifi_is_connected,wifi_timeout>0,win_wifi)

			battery_percent = onboard.get_battery_percentage()
			draw_battery(sty_tb.background(),battery_percent,win_bv)

			inactivity += 1

			# turn off after some period
			# takes longer to turn off in the 'used' position
			if ugfx.orientation() == 180:
				inactivity_limit = 120
			else:
				inactivity_limit = 30
			if battery_percent > 120:  #if charger plugged in
				if ugfx.backlight() == 0:
					ugfx.power_mode(ugfx.POWER_ON)
				ugfx.backlight(100)
			elif inactivity > inactivity_limit:
				low_power()
			else:
				backlight_adjust()

			ledg.off()

		for hook in external_hooks:
			try:
				if hook["needs_wifi"] and not wifi.nic().is_connected():
					continue;

				if hook["next_tick_at"] < pyb.millis():
					text = None
					if "icon" in hook:
						text = hook["tick"](hook["icon"])
					else:
						text = hook["tick"]()
					hook["next_tick_at"] = pyb.millis() + hook["period"]
					if text:
						if hook_feeback.count() > 10:
							hook_feeback.remove_item(0)
						hook_feeback.add_item(text)
						if hook_feeback.selected_index() >= (hook_feeback.count()-2):
							hook_feeback.selected_index(hook_feeback.count()-1)
			except Exception as e:  # if anything in the hook fails to work, we need to skip it
				print ("%s in %s background task. Not running again until next reboot! " % (type(e).__name__, hook['name']))
				sys.print_exception(e)
				external_hooks.remove(hook)
				continue

		if buttons.is_pressed("BTN_MENU"):
			pyb.delay(20)
			break
		if buttons.is_pressed("BTN_A"):
			inactivity = 0
			tick = True
		if buttons.is_pressed("BTN_B"):
			inactivity = 0
			tick = True


	for hook in external_hooks:
		if "icon" in hook:
			hook["icon"].destroy()
	for w in windows:
		w.destroy()
	apps.home.draw_name.draw_destroy(obj_name)
	win_name.destroy()
	hook_feeback.destroy()
	if ugfx.backlight() == 0:
		ugfx.power_mode(ugfx.POWER_ON)
	ugfx.backlight(100)
	ugfx.orientation(180)

	#if we havnt connected yet then give up since the periodic function wont be poked
	if wifi_timeout >= 0: # not (wifi.nic().is_connected()):
		wifi.nic().disconnect()

while True:
	# By separating most of the work in a function we save about 1,6kb memory
	home_main()
	gc.collect()
	execfile("apps/home/quick_launch.py")
