import pyb
import math

# Example of how a simple animation can be done
# ToDo: This is quite flickery. It would work a lot better with
#       Pixmaps, but I couldn't get them to work :(

lcd = pyb.UGFX()

sec = 0;

def draw_hand(lcd, cx, cy, angle, length, thickness, color):
    x = int(math.cos(angle) * length + cx);
    y = int(math.sin(angle) * length + cy);
    lcd.thickline(cx, cy, x, y, color, thickness, 1)

while True:
    lcd.area(0, 0, lcd.get_width(), lcd.get_height(), 0)

    # Center
    cx = int(lcd.get_width() / 2);
    cy = int(lcd.get_height() / 2);

    # Clock face
    lcd.circle(cx, cy, 70, pyb.UGFX.WHITE)
    for i in range(0, 12):
        a = math.pi * 2 * i / 12
        x1 = int(math.cos(a) * 55 + cx);
        y1 = int(math.sin(a) * 55 + cy);
        x2 = int(math.cos(a) * 60 + cx);
        y2 = int(math.sin(a) * 60 + cy);
        lcd.line(x1, y1, x2, y2, pyb.UGFX.WHITE)

    # Hand: hours
    angel_hour = math.pi * 2 * sec / 60 / 60 / 12 - math.pi / 2
    draw_hand(lcd, cx, cy, angel_hour, 35, 4, pyb.UGFX.YELLOW)

    # Hand: minutes
    angel_min = math.pi * 2 * sec / 60 / 60 - math.pi / 2
    draw_hand(lcd, cx, cy, angel_min, 40, 2, pyb.UGFX.WHITE)

    # Hand: seconds
    angel_seconds = math.pi * 2 * sec / 60 - math.pi / 2
    draw_hand(lcd, cx, cy, angel_seconds, 50, 1, pyb.UGFX.RED)

    # Wait
    pyb.delay(10)

    sec += 1;