import pyb
import math
import ugfx

ugfx.init()
ugfx.orientation(270)

grid_size = 8;
body_colour = ugfx.RED
back_colour = 0;
food_colour = ugfx.YELLOW
wall_colour = ugfx.BLUE
score = 0;
edge_x = math.floor(ugfx.width()/grid_size)-2;
edge_y = math.floor(ugfx.height()/grid_size)-2;

def disp_square(x,y,colour):
	ugfx.area((x+1)*grid_size, (y+1)*grid_size, grid_size, grid_size, colour) 
	
def disp_body_straight(x,y,rotation,colour):
	if (rotation == 0):
		ugfx.area((x+1)*grid_size+1, (y+1)*grid_size+1, grid_size-2, grid_size, colour) 
	elif (rotation == 90):
		ugfx.area((x+1)*grid_size+1, (y+1)*grid_size+1, grid_size, grid_size-2, colour) 
	elif (rotation == 180):
		ugfx.area((x+1)*grid_size+1, (y+1)*grid_size-1, grid_size-2, grid_size, colour) 
	else:
		ugfx.area((x+1)*grid_size-1, (y+1)*grid_size+1, grid_size, grid_size-2, colour) 
	
def disp_eaten_food(x,y,colour):
	ugfx.area((x+1)*grid_size, (y+1)*grid_size, grid_size, grid_size, colour)

def randn_square():
	return  [pyb.rng()%edge_x, pyb.rng()%edge_y]

body_x = [12,13,14,15,16]
body_y = [2,2,2,2,2]

ugfx.area(0,0,ugfx.width(),ugfx.height(),0)

ugfx.area(0,0,grid_size*(edge_x+1),grid_size,wall_colour)
ugfx.area(0,0,grid_size,grid_size*(edge_y+1),wall_colour)
ugfx.area(grid_size*(edge_x+1),0,grid_size,grid_size*(edge_y+1),wall_colour)
ugfx.area(0,grid_size*(edge_y+1),grid_size*(edge_x+2),grid_size,wall_colour)

keepgoing = 10;

food = [20,20]
disp_square(food[0],food[1],food_colour)
 
j_up = pyb.Pin("JOY_UP", pyb.Pin.IN)
j_down = pyb.Pin("JOY_DOWN", pyb.Pin.IN)
j_left = pyb.Pin("JOY_LEFT", pyb.Pin.IN)
j_right = pyb.Pin("JOY_RIGHT", pyb.Pin.IN)
btn_menu = pyb.Pin("BTN_MENU", pyb.Pin.IN)

j_up.init(pyb.Pin.IN, pull=pyb.Pin.PULL_DOWN)
j_down.init(pyb.Pin.IN, pull=pyb.Pin.PULL_DOWN)
j_left.init(pyb.Pin.IN, pull=pyb.Pin.PULL_DOWN)
j_right.init(pyb.Pin.IN, pull=pyb.Pin.PULL_DOWN)
btn_menu.init(pyb.Pin.IN, pull=pyb.Pin.PULL_UP)
dir_x = 1
dir_y = 0
orient = 270

#for i in range(0,len(body_x)):
#	disp_body_straight(body_x[i],body_y[i],orient,body_colour)
	

while(keepgoing > 0):
	
	if (j_left.value()):
		if (dir_x > -1):
			dir_x = 1;
			dir_y = 0;
			orient = 270
	if (j_right.value()):
		if (dir_x < 1):
			dir_x = -1;
			dir_y = 0;
			orient = 90
	if (j_down.value()):
		if (dir_y > -1):
			dir_y = 1;
			dir_x = 0;
			orient = 180
	if (j_up.value()):
		if (dir_y < 1):
			dir_y = -1;
			dir_x = 0;	
			orient = 0
	
	
	body_x.append(body_x[-1]+dir_x)
	body_y.append(body_y[-1]+dir_y)
	
	for i in range(0,len(body_x)-1):
		if (body_x[i] == body_x[-1]) and (body_y[i] == body_y[-1]):
			keepgoing = 0;
	
	
	if not((body_x[-1] == food[0]) and (body_y[-1] == food[1])):
		x_del = body_x.pop(0)
		y_del = body_y.pop(0)
		disp_eaten_food(x_del,y_del,back_colour)
	else:
		disp_eaten_food(food[0],food[1],body_colour)
		food = randn_square()
		disp_square(food[0],food[1],food_colour)
		score = score + 1
		

	disp_body_straight(body_x[-1],body_y[-1],orient,body_colour)


	if ((body_x[-1] >= edge_x) or (body_x[-1] < 0) or (body_y[-1] >= edge_y) or (body_y[-1] < 0)):
		keepgoing = 0;

		
	if (btn_menu.value() == 0):
		keepgoing = 0;
	
	pyb.delay(100)
	
#	keepgoing = keepgoing - 1

ugfx.area(0,0,ugfx.width(),ugfx.height(),0)
ugfx.text(30, 30, "GAME OVER Score: %d" % (score), 0xFFFF)