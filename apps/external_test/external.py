import ugfx

period = 1 * 1000
needs_icon = True

i = 0
def tick(icon):
	global i
	i += 1
	icon.show()
	ugfx.set_default_font("c*")
	icon.area(0, 0, icon.width(), icon.height(), 0xFFFF)
	icon.text(0, 0, str(i), 0)

	return "Test: %d"% i
