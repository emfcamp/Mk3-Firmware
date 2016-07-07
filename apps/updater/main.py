### author: emf badge team
### description: updates and installs apps. To manage your list of apps use https://badge.emf.camp
### license: MIT

import ugfx

ugfx.init()
ugfx.area(0, 0, ugfx.width(), ugfx.height(), ugfx.BLACK)
ugfx.text(0, 0, "Checking for app updates...", ugfx.RED)

# ToDo: Actually do that