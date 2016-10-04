### Author: EMF Badge team
### Description: Change your name
### Category: Settings
### License: MIT
### Appname : Change name

import dialogs
from database import Database
import buttons
import ugfx

ugfx.init()
buttons.init()

with Database() as db:
    name = db.get("display-name", "")
    name_new = dialogs.prompt_text("Enter your name", init_text=name, width = 310, height = 220)
    if name_new:
        db.set("display-name", name_new)
