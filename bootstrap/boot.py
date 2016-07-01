# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import pyb
import json

def get_config():
    with open("config.json") as data_file:
        return json.loads(data_file.read())

config = get_config();

app = config["current"];

lcd = pyb.UGFX()
lcd.text("Loading '" + app + "'...", 40, 40, pyb.UGFX.WHITE)
lcd.text("Press MENU to open the loader", 40, 60, pyb.UGFX.RED)

pyb.delay(2000)

# If MENU button is pressed go to "store" instead
btn_menu = pyb.Pin("BTN_MENU", pyb.Pin.IN)
btn_menu.init(pyb.Pin.IN, pull=pyb.Pin.PULL_UP)

if (btn_menu.value() == 0):
    app = "store";
    lcd.area(0, 0, lcd.get_width(), lcd.get_height(), 0)
    lcd.text("Opening store...", 40, 60, pyb.UGFX.WHITE)
    pyb.delay(1000)

# Clear screen
lcd.area(0, 0, lcd.get_width(), lcd.get_height(), 0)


pyb.main("apps/%s.py" % (app))


# pyb.main("blink/main.py")
# main script to run after this one
#pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
#pyb.usb_mode('CDC+HID') # act as a serial device and a mouse
