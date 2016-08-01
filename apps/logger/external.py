from filesystem import *
from database import *
import pyb
import stm
import ugfx
import http_client
import socket
import network
import wifi
import gc

adc_obj = pyb.ADC(pyb.Pin("ADC_UNREG"))
ref_obj = pyb.ADC(0)
temp_obj = pyb.ADC(17)
light_obj = pyb.ADC(16)

update_rate = 15

i=0

def get_battery_voltage(adc_obj, ref_obj):
	vin = adc_obj.read()
	ref_reading = ref_obj.read()
	factory_reading = stm.mem16[0x1FFF75AA]
	reference_voltage = factory_reading/4095*3
	supply_voltage = 4095/ref_reading*reference_voltage 
	return 2 * vin / 4095 * supply_voltage
	
def get_light(light_obj):
	return light_obj.read()


def periodic_home(icon):
	global adc_obj
	global ref_obj
	global temp_obj
	global light_obj
	global i
	icon.show()
	ugfx.set_default_font("c*")
	icon.area(0,0,icon.width(),icon.height(),0xFFFF)
	icon.text(0,0,str(i),0)
	i+=1
	
	bv = get_battery_voltage(adc_obj, ref_obj)
	li = get_light(light_obj)
	
	logfile = "log.txt"
	


	if database_get("stats_upload", 0):
		urlparams = "origin=PBADGE0&data=0bV" + str(bv) + "%5BPBADGE0%5D"
		try:
			if wifi.nic().is_connected():
				with http_client.post('http://ukhas.net/api/upload', urlencoded=urlparams) as resp:
					pass
		except OSError as e:
			print("Upload failed " + str(e))

		
		
	try:
		if not is_file(logfile):
			with open(logfile, "w") as f:
				f.write("vbat, light \r\n")
		
		with open(logfile, "a") as f:
			f.write(str(bv) + ", " + str(li) + "\r\n")
	except OSError as e:
		print("Logging failed: " + str(e))
		return "Logging failed"
		
		
	return "Logged " + str(bv)