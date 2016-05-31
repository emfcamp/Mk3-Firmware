
#light sensor is on PA3 (note change this)
a = pyb.ADC('PA3')

while True:
	print(str(a.read()))
	pyb.delay(1000)