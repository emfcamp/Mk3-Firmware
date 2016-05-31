import pyb

t4 = pyb.Timer(4, freq=100, mode=pyb.Timer.CENTER)

for x in range(1,90):

	t4.freq(x*100)
	ch1 = t4.channel(1, pyb.Timer.PWM, pin=pyb.Pin.board.PD12, pulse_width=(t4.period() + 1) // 2)
	
	pyb.delay(100)

pyb.Pin("PD12",pyb.Pin.OUT).low()