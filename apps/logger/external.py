from filesystem import *
import pyb
import stm

adc_obj = pyb.ADC(pyb.Pin("ADC_UNREG"))
ref_obj = pyb.ADC(0)
temp_obj = pyb.ADC(17)

def get_battery_voltage(adc_obj, ref_obj):
	vin = adc_obj.read()
	ref_reading = ref_obj.read()
	factory_reading = stm.mem16[0x1FFF75AA]
	reference_voltage = factory_reading/4095*3
	supply_voltage = 4095/ref_reading*reference_voltage 
	return 2 * vin / 4095 * supply_voltage

def periodic_home():
	global adc_obj
	global ref_obj
	global temp_obj
	
	bv = get_battery_voltage(adc_obj, ref_obj)
	
	logfile = "log.txt"
	
	if not is_file(logfile):
		with open(logfile, "w") as f:
			f.write("Battery voltage, \r\n")
	
	with open(logfile, "a") as f:
		f.write(str(bv) + ",\r\n")