### author: emf badge team
### description: updates and installs apps. To manage your list of apps use https://badge.emf.camp
### license: MIT
### depends: http_client, badge

import ugfx
import os
import pyb
import badge

ugfx.init()

ugfx.area(0, 0, ugfx.width(), ugfx.height(), ugfx.BLACK)
ugfx.text(0, 0, "TiLDA App Updater", ugfx.RED)
ugfx.text(0, 30, "Checking your list of apps...", ugfx.WHITE)

