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


def get_unreg_voltage():
	global adc_obj, ref_obj
	vin = adc_obj.read()
	ref_reading = ref_obj.read()
	factory_reading = stm.mem16[0x1FFF75AA]
	reference_voltage = factory_reading/4095*3
	supply_voltage = 4095/ref_reading*reference_voltage
	return 2 * vin / 4095 * supply_voltage

def get_battery_voltage():
	global vbat_obj, ref_obj
	vin = vbat_obj.read()
	ref_reading = ref_obj.read()
	factory_reading = stm.mem16[0x1FFF75AA]
	reference_voltage = factory_reading/4095*3
	supply_voltage = 4095/ref_reading*reference_voltage
	return 6 * vin / 4095 * supply_voltage

def get_battery_percentage():
	v = get_unreg_voltage()
	return int( (v-3.7) / (4.15-3.7) * 100)
	
def get_light():
	global light_obj
	return light_obj.read()

adc_obj = pyb.ADC(pyb.Pin("ADC_UNREG"))
ref_obj = pyb.ADC(0)
temp_obj = pyb.ADC(17)
vbat_obj = pyb.ADC(18)
light_obj = pyb.ADC(16)

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

	
def run_app(path):
	try:
		mod = __import__(path)
		if "main" in dir(mod):
			mod.main()
	except Exception as e:
		import sys
		import uio
		import ugfx
		s = uio.StringIO()
		sys.print_exception(e, s)
		ugfx.clear()
		ugfx.set_default_font(ugfx.FONT_SMALL)
		w=ugfx.Container(0,0,ugfx.width(),ugfx.height())
		l=ugfx.Label(0,0,ugfx.width(),ugfx.height(),s.getvalue(),parent=w)
		w.show()
		raise(e)
	
def reset_and_run(path):
	if stm.mem8[0x40002851] == 0x5B:
		stm.mem8[0x40002851] = 0
		return
	import struct
	memloc = 0x40002854
	mem_max = memloc + 120
	for s in path:
		bytes = struct.pack("s",s)
		for b in bytes:
			stm.mem8[memloc] = b
			memloc += 1
			if (memloc >= mem_max):
				stm.mem8[0x40002850] = 0x5A
				stm.mem8[memloc] = 0
				pyb.hard_reset()
			
	stm.mem8[0x40002851] = 0x5A
	stm.mem8[memloc] = 0
	
	pyb.hard_reset()
			
	