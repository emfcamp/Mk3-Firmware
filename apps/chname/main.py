### Author: EMF Badge team
### Description: Snake!
### Category: Settings
### License: MIT
### Appname : Change Name

import pyb
from dialogs import *
from database import *

timer = pyb.Timer(3)
timer.init(freq=60)
timer.callback(lambda t:ugfx.poll())

name = database_get("display-name", "")

name_new = prompt_text("Enter your name", default=name, init_text = name, true_text="OK", false_text="Back", width = 310, height = 220)

database_set("display-name", name_new)


timer.deinit()