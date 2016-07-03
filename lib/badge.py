import pyb

class Badge:

	switch_menu = None
	switch_a = None
	switch_b = None
	switch_up = None
	switch_down = None
	switch_left = None
	switch_right = None
	switch_center = None
	
	int_menu = None
	int_a = None
	int_b = None
	int_up = None
	int_down = None
	int_left = None
	int_right = None
	int_center = None

	#def __init__(self):
	
	def is_pressed(self, int_in):
		if int_in == "JOY_UP":
			return self.switch_up.value() > 0
		elif int_in == "JOY_DOWN":
			return self.switch_down.value() > 0
		elif int_in == "JOY_LEFT":
			return self.switch_left.value() > 0
		elif int_in == "JOY_RIGHT":
			return self.switch_right.value() > 0
		elif int_in == "JOY_CENTER":
			return self.switch_center.value() > 0
		elif int_in == "BTN_A":
			return self.switch_a.value() == 0
		elif int_in == "BTN_B":
			return self.switch_b.value() == 0
		elif int_in == "BTN_MENU":
			return self.switch_menu.value() == 0

		
	def disable_interrupts(self):
		
		self.int_up = pyb.ExtInt(self.switch_up, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, None)		
		self.int_down = pyb.ExtInt(self.switch_down, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, None)		
		self.int_right = pyb.ExtInt(self.switch_right, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, None)
		self.int_left = pyb.ExtInt(self.switch_left, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, None)		
		self.int_center = pyb.ExtInt(self.switch_center, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, None)		
		self.int_menu = pyb.ExtInt(self.switch_menu, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, None)		
		self.int_a = pyb.ExtInt(self.switch_a, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, None)		
		self.int_b = pyb.ExtInt(self.switch_b, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, None)
		
		self.switch_menu.init(pyb.Pin.IN, pyb.Pin.PULL_UP)
		self.switch_a.init(pyb.Pin.IN, pyb.Pin.PULL_UP)
		self.switch_b.init(pyb.Pin.IN, pyb.Pin.PULL_UP)
		
		self.switch_up.init(pyb.Pin.IN, pyb.Pin.PULL_DOWN)
		self.switch_down.init(pyb.Pin.IN, pyb.Pin.PULL_DOWN)
		self.switch_right.init(pyb.Pin.IN, pyb.Pin.PULL_DOWN)
		self.switch_left.init(pyb.Pin.IN, pyb.Pin.PULL_DOWN)
		self.switch_center.init(pyb.Pin.IN, pyb.Pin.PULL_DOWN)
			
	def init_pins(self):
	
		self.switch_up = pyb.Pin("JOY_UP", pyb.Pin.IN)
		self.switch_down = pyb.Pin("JOY_DOWN", pyb.Pin.IN)
		self.switch_right = pyb.Pin("JOY_RIGHT", pyb.Pin.IN)
		self.switch_left = pyb.Pin("JOY_LEFT", pyb.Pin.IN)
		self.switch_center = pyb.Pin("JOY_CENTER", pyb.Pin.IN)
		self.switch_menu = pyb.Pin("BTN_MENU", pyb.Pin.IN)
		self.switch_a = pyb.Pin("BTN_A", pyb.Pin.IN)
		self.switch_b = pyb.Pin("BTN_B", pyb.Pin.IN)
		
		self.switch_menu.init(pyb.Pin.IN, pyb.Pin.PULL_UP)
		self.switch_a.init(pyb.Pin.IN, pyb.Pin.PULL_UP)
		self.switch_b.init(pyb.Pin.IN, pyb.Pin.PULL_UP)
		
		self.switch_up.init(pyb.Pin.IN, pyb.Pin.PULL_DOWN)
		self.switch_down.init(pyb.Pin.IN, pyb.Pin.PULL_DOWN)
		self.switch_right.init(pyb.Pin.IN, pyb.Pin.PULL_DOWN)
		self.switch_left.init(pyb.Pin.IN, pyb.Pin.PULL_DOWN)
		self.switch_center.init(pyb.Pin.IN, pyb.Pin.PULL_DOWN)
		


	def set_interrupt(self,int_in, interrupt):
		#ideally also needs edge_pressed and edge_released	
		if int_in == "JOY_UP":
			self.int_up = pyb.ExtInt(self.switch_up, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, interrupt)
		elif int_in == "JOY_DOWN":
			self.int_down = pyb.ExtInt(self.switch_down, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, interrupt)
		elif int_in == "JOY_LEFT":
			self.int_left = pyb.ExtInt(self.switch_left, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, interrupt)
		elif int_in == "JOY_RIGHT":
			self.int_right = pyb.ExtInt(self.switch_right, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, interrupt)
		elif int_in == "JOY_CENTER":
			self.int_center = pyb.ExtInt(self.switch_center, pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, interrupt)
		elif int_in == "BTN_A":
			self.int_a = pyb.ExtInt(self.switch_a, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, interrupt)
		elif int_in == "BTN_B":
			self.int_b = pyb.ExtInt(self.switch_b, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, interrupt)
		elif int_in == "BTN_MENU":
			self.int_menu = pyb.ExtInt(self.switch_menu, pyb.ExtInt.IRQ_FALLING, pyb.Pin.PULL_UP, interrupt)

		