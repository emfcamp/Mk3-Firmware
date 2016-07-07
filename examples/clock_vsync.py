import pyb
import math
import ugfx

# Example of how a simple animation can be done
# ToDo: This is quite flickery. It would work a lot better with
#       Pixmaps, but I couldn't get them to work :(

ugfx.init()
ugfx.enable_tear()
tear = pyb.Pin("TEAR", pyb.Pin.IN)
ugfx.set_tear_line((int(320/2)+0))
ugfx.area(0,0,ugfx.width(), ugfx.height(), 0)
sec = 0;

def draw_hand(cx, cy, angle, length, thickness, color):
    x = int(math.cos(angle) * length + cx);
    y = int(math.sin(angle) * length + cy);
    ugfx.thickline(cx, cy, x, y, color, thickness, 1)

while True:
    

    # Center
    cx = int(ugfx.width() / 2);
    cy = int(ugfx.height() / 2);


    # Hand: hours
    angel_hour = math.pi * 2 * sec / 60 / 60 / 12 - math.pi / 2    

    # Hand: minutes
    angel_min = math.pi * 2 * sec / 60 / 60 - math.pi / 2    

    # Hand: seconds
    angel_seconds = math.pi * 2 * sec / 60 - math.pi / 2
    
    # wait for vsync
    while(tear.value() == 0):
        2+2 
    while(tear.value()):
        2+2 
    #Do all the drawing at once    
    ugfx.area(cx-71, cy-71, 141, 141, 0)
	# Hands
    draw_hand(cx, cy, angel_hour, 35, 4, ugfx.YELLOW)
    draw_hand(cx, cy, angel_seconds, 50, 1, ugfx.RED)
    draw_hand(cx, cy, angel_min, 40, 2, ugfx.WHITE)
    # Clock face
    ugfx.circle(cx, cy, 70, ugfx.WHITE)
    for i in range(0, 12):
        a = math.pi * 2 * i / 12
        x1 = int(math.cos(a) * 55 + cx);
        y1 = int(math.sin(a) * 55 + cy);
        x2 = int(math.cos(a) * 60 + cx);
        y2 = int(math.sin(a) * 60 + cy);
        ugfx.line(x1, y1, x2, y2, ugfx.WHITE)

    
    # Wait
    pyb.delay(10)

    sec += 1;
    
ugfx.disable_tear()