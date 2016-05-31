import pyb
import math

l=pyb.UGFX()
l.set_orientation(270)

grid_size = 8;
body_colour = pyb.UGFX.RED
back_colour = 0;
food_colour = pyb.UGFX.YELLOW
score = 0;
edge_x = math.floor(l.get_width()/grid_size);
edge_y = math.floor(l.get_height()/grid_size);

def disp_square(x,y,colour):
	l.area(x*grid_size, y*grid_size, grid_size, grid_size, colour) 
	
def randn_square():
	return  [pyb.rng()%edge_x, pyb.rng()%edge_y]

body_x = [2,2,2]
body_y = [12,13,14]

l.area(0,0,l.get_width(),l.get_height(),0)

for i in range(0,len(body_x)):
	disp_square(body_x[i],body_y[i],body_colour)
	

keepgoing = 10;

food = [20,20]
disp_square(food[0],food[1],food_colour)

j_up = pyb.Pin(pyb.Pin.board.PD6, pyb.Pin.IN)
j_down = pyb.Pin(pyb.Pin.board.PD11, pyb.Pin.IN)
j_left = pyb.Pin(pyb.Pin.board.PA15, pyb.Pin.IN)
j_right = pyb.Pin(pyb.Pin.board.PD3, pyb.Pin.IN)
btn_menu = pyb.Pin(pyb.Pin.board.PD10, pyb.Pin.IN)

j_up.init(pyb.Pin.IN, pull=pyb.Pin.PULL_DOWN)
j_down.init(pyb.Pin.IN, pull=pyb.Pin.PULL_DOWN)
j_left.init(pyb.Pin.IN, pull=pyb.Pin.PULL_DOWN)
j_right.init(pyb.Pin.IN, pull=pyb.Pin.PULL_DOWN)
btn_menu.init(pyb.Pin.IN, pull=pyb.Pin.PULL_UP)
dir_x = 1
dir_y = 0
while(keepgoing > 0):
	
	
	if (j_left.value()):
		if (dir_x > -1):
			dir_x = 1;
			dir_y = 0;
	if (j_right.value()):
		if (dir_x < 1):
			dir_x = -1;
			dir_y = 0;
	if (j_down.value()):
		if (dir_y > -1):
			dir_y = 1;
			dir_x = 0;
	if (j_up.value()):
		if (dir_y < 1):
			dir_y = -1;
			dir_x = 0;		
	
	
	body_x.append(body_x[-1]+dir_x)
	body_y.append(body_y[-1]+dir_y)
	
	for i in range(0,len(body_x)-1):
		if (body_x[i] == body_x[-1]) and (body_y[i] == body_y[-1]):
			keepgoing = 0;
	
	
	if not((body_x[-1] == food[0]) and (body_y[-1] == food[1])):
		x_del = body_x.pop(0)
		y_del = body_y.pop(0)
		disp_square(x_del,y_del,back_colour)
	else:
		food = randn_square()
		disp_square(food[0],food[1],food_colour)
		score = score + 1

	disp_square(body_x[-1],body_y[-1],body_colour)

	if ((body_x[-1] >= edge_x) or (body_x[-1] < 0) or (body_y[-1] >= edge_y) or (body_y[-1] < 0)):
		keepgoing = 0;

		
	if (btn_menu.value() == 0):
		keepgoing = 0;
	
	pyb.delay(100)
	
#	keepgoing = keepgoing - 1
l.area(0,0,l.get_width(),l.get_height(),0)
l.text("GAME OVER Score: " + str(score) ,30,30,0xFFFF)
