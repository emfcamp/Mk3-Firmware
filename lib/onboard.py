import pyb
import stm

def get_temperature():
	global adc_obj, ref_obj
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

def get_battery_voltage():
	global adc_obj, ref_obj
	vin = adc_obj.read()
	ref_reading = ref_obj.read()
	factory_reading = stm.mem16[0x1FFF75AA]
	reference_voltage = factory_reading/4095*3
	supply_voltage = 4095/ref_reading*reference_voltage
	return 2 * vin / 4095 * supply_voltage

def get_battery_percentage():
	v = get_battery_voltage()
	return int( (v-3.7) / (4.15-3.7) * 100)

adc_obj = pyb.ADC(pyb.Pin("ADC_UNREG"))
ref_obj = pyb.ADC(0)
temp_obj = pyb.ADC(17)

def hide_splash_on_next_boot(hide=True):
	if hide:
		stm.mem8[0x40002850] = 0x9C
	else:
		stm.mem8[0x40002850] = 0x00

def is_splash_hidden():
	return stm.mem8[0x40002850] == 0x9C

def semihard_reset():
	hide_splash_on_next_boot()
	pyb.hard_reset()
