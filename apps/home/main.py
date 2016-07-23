import ugfx
import pyb
import os
from database import *
from filesystem import *
import buttons
import gc
import stm
import apps.home.draw_name

	
def draw_battery(x,y,back_colour,percent):
	ugfx.set_default_font("c*")	
	ugfx.area(x+35,y,40,25,back_colour)
	if percent <= 120:
		ugfx.text(x+35,y,str(int(min(percent,100))),back_colour^0xFFFF)	
	y += 2
	ugfx.area(x,y,30,11,back_colour^0xFFFF)
	ugfx.area(x+30,y+3,3,5,back_colour^0xFFFF)
	
	if percent > 120:
		ugfx.area(x+2,y+2,26,7,ugfx.YELLOW)
	elif percent > 2:
		ugfx.area(x+2,y+2,26,7,back_colour)
		ugfx.area(x+2,y+2,int(min(percent,100)*26/100),7,back_colour^0xFFFF)
	else:
		ugfx.area(x+2,y+2,26,7,ugfx.RED)
	

tick = 1
	
def tick_inc(t):
	global tick
	tick += 1
	
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
ugfx.area(0,0,320,240,0)
stm.mem8[0x40002850] = 0
	

while True:
#	ugfx.init()
	
	win_name = ugfx.Container(0,40,320,200)
	ugfx.clear()
	obj_name = apps.home.draw_name.draw(win_name)

	buttons.init()
	
	gc.collect()
	
	
	
	adc_obj = pyb.ADC(pyb.Pin("ADC_UNREG"))
	ref_obj = pyb.ADC(0)
	temp_obj = pyb.ADC(17)
	
	min_ctr = 0
	
	timerb = pyb.Timer(3)
	timerb.init(freq=1)
	timerb.callback(tick_inc)
	
	
	ext_list = get_home_screen_background_apps()
	ext_import = []
	per_freq=[];
	for e in ext_list:
		ext_import.append(__import__(e[:-3]))
		try:
			per_freq.append(ext_import[-1].update_rate)
		except AttributeError:
			per_freq.append(120)
			
	per_time_since = [0]*len(ext_import)
	
	while True:
		pyb.wfi()
		
		if tick > 0:
			tick = 0
			backlight_adjust()
			
			v = get_battery_voltage(adc_obj,ref_obj)
			#t = get_temperature(temp_obj,ref_obj)
			#print(t)
			draw_battery(3,3,0xFFFF,int((v-3.7)/(4.15-3.7)*100))
			
			min_ctr += 1
			
			if (min_ctr == 30):
				min_ctr = 0
				
				for i in range(0, len(ext_import)):
					per_time_since[i] += 30
					if per_time_since[i] >= per_freq[i]:
						per_time_since[i] = 0				
						e = ext_import[i]					
						if "periodic_home" in dir(e):
							e.periodic_home()

		if buttons.is_triggered("BTN_MENU"):
			break

	
	apps.home.draw_name.draw_destroy(obj_name)
	win_name.destroy()
	timerb.deinit()
	ugfx.backlight(100)

	## ToDo: Maybe boot should always chdir to the app folder?
	execfile("apps/home/quick_launch.py")
	
