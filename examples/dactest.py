dac = DAC(2)

countdown = 10

while (countdown):
	dac.write(countdown*20)
	
	pyb.delay(300)
	
	countdown -= 10