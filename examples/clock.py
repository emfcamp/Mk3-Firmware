import pyb
import math
import ugfx

# Example of how a simple animation can be done
# ToDo: This is quite flickery. It would work a lot better with
#       Pixmaps, but I couldn't get them to work :(

ugfx.init()
ugfx.write_command(0x35,0)
ugfx.write_command(0x36,0x08)
tear = pyb.Pin("TEAR", pyb.Pin.IN)
sec = 0;

def draw_hand(cx, cy, angle, length, thickness, color):
    x = int(math.cos(angle) * length + cx);
    y = int(math.sin(angle) * length + cy);
    ugfx.thickline(cx, cy, x, y, color, thickness, 1)

while True:
    ugfx.area(0, 0, ugfx.width(), ugfx.height(), 0)

    # Center
    cx = int(ugfx.width() / 2);
    cy = int(ugfx.height() / 2);

    # Clock face
    ugfx.circle(cx, cy, 70, ugfx.WHITE)
    for i in range(0, 12):
        a = math.pi * 2 * i / 12
        x1 = int(math.cos(a) * 55 + cx);
        y1 = int(math.sin(a) * 55 + cy);
        x2 = int(math.cos(a) * 60 + cx);
        y2 = int(math.sin(a) * 60 + cy);
        ugfx.line(x1, y1, x2, y2, ugfx.WHITE)

    # Hand: hours
    angel_hour = math.pi * 2 * sec / 60 / 60 / 12 - math.pi / 2
    draw_hand(cx, cy, angel_hour, 35, 4, ugfx.YELLOW)

    # Hand: minutes
    angel_min = math.pi * 2 * sec / 60 / 60 - math.pi / 2
    draw_hand(cx, cy, angel_min, 40, 2, ugfx.WHITE)

    # Hand: seconds
    angel_seconds = math.pi * 2 * sec / 60 - math.pi / 2
    draw_hand(cx, cy, angel_seconds, 50, 1, ugfx.RED)

    # Wait
    #pyb.delay(10)
    while(tear.value() == 0):
        2+2 
    while(tear.value()):
        2+2 

    sec += 1;