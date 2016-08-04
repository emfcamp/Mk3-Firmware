### Author: EMF Badge team
### Description: Shows all the sponsors that have helped make this badge possible
### Category: Other
### License: MIT

import ugfx, pyb, buttons

ugfx.init()
ugfx.clear()
buttons.init()
ugfx.set_default_font(ugfx.FONT_NAME)

def screen_1():
    ugfx.display_image(0, 0, "splash1.bmp")

def screen_2():
    ugfx.display_image(0, 0, "apps/sponsors/sponsors.gif")

def screen_3():
    ugfx.clear(ugfx.html_color(0x7c1143))
    ugfx.text(27, 90, "Thank you!", ugfx.WHITE)

SCREENS = [screen_1, screen_2, screen_3]
SCREEN_DURATION = 2000

screen_index = -1
next_change = 0;
while True:
    if pyb.millis() > next_change:
        screen_index = (screen_index + 1) % len(SCREENS)
        SCREENS[screen_index]()
        next_change = pyb.millis() + SCREEN_DURATION
    pyb.wfi()
    if buttons.is_triggered("BTN_MENU") or buttons.is_triggered("BTN_A") or buttons.is_triggered("BTN_B") or buttons.is_triggered("JOY_CENTER"):
        break;

ugfx.clear()



