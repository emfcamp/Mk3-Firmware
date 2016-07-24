import buttons
import ugfx

up = 0
down = 0
left = 0
right = 0

def callback_arrow_up(line):
	global up
	up = 1

def callback_arrow_down(line):
	global down
	down = 1

def callback_arrow_right(line):
	global left
	left = 1

def callback_arrow_left(line):
	global right
	right = 1

buttons.init()
buttons.enable_interrupt("JOY_UP", callback_arrow_up)
buttons.enable_interrupt("JOY_DOWN", callback_arrow_down)
buttons.enable_interrupt("JOY_LEFT", callback_arrow_left)
buttons.enable_interrupt("JOY_RIGHT", callback_arrow_right)

while True:
    if up:
        up = 0
        ugfx.area(40,0,20,20,0)
    #else:
    #    ugfx.area(40,0,20,20,0xFFFF)
    #    up = 0

    if down:
        down = 0
        ugfx.area(40,50,20,20,0)
    #else:
#        down = 0
#        ugfx.area(40,50,20,20,0xFFFF)

    if right:
        right = 0
        ugfx.area(70,25,20,20,0)
#    else:
#        right = 0
#        ugfx.area(70,25,20,20,0xFFFF)

    if left:
        left = 0
        ugfx.area(10,25,20,20,0)
#    else:
#        left = 0
#        ugfx.area(10,25,20,20,0xFFFF)


    if buttons.is_pressed("JOY_UP"):
        ugfx.area(140,0,20,20,0)
    else:
        ugfx.area(140,0,20,20,0xFFFF)
        #ugfx.area(40,0,20,20,0xFFFF)

    if buttons.is_pressed("JOY_DOWN"):
        ugfx.area(140,50,20,20,0)
    else:
        ugfx.area(140,50,20,20,0xFFFF)
        #ugfx.area(40,50,20,20,0xFFFF)

    if buttons.is_pressed("JOY_RIGHT"):
        ugfx.area(170,25,20,20,0)
    else:
        ugfx.area(170,25,20,20,0xFFFF)
        #ugfx.area(70,25,20,20,0xFFFF)

    if buttons.is_pressed("JOY_LEFT"):
        ugfx.area(110,25,20,20,0)
    else:
        ugfx.area(110,25,20,20,0xFFFF)
        #ugfx.area(10,25,20,20,0xFFFF)
