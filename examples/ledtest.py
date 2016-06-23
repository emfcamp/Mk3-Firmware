ledr = pyb.Pin("LED_RED",pyb.Pin.OUT)
ledg = pyb.Pin("LED_GREEN",pyb.Pin.OUT)
ledt = pyb.Pin("LED_TORCH",pyb.Pin.OUT)
ledb = pyb.Pin("LED_BACKLIGHT",pyb.Pin.OUT)

timer = pyb.Timer(17, freq=1000)
ch1 = timer.channel(1, pyb.Timer.PWM, pin=ledb, pulse_width=0)

ledt.high()

countdown = 10;
while (countdown):
	
	ch1.pulse_width_percent(100-(countdown*10))
	ledr.high()
	ledg.low()
	pyb.delay(200)
	
	ledr.low()
	ledg.high()
	pyb.delay(200)
	
	countdown-=1;
	

