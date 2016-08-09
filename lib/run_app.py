def run_app(path):
#	buttons.enable_menu_reset()
	try:
		mod = __import__(path)
		if "main" in dir(mod):
			mod.main()
	except Exception as e:
		import sys
		import uio
		import ugfx
		s = uio.StringIO()
		sys.print_exception(e, s)
		ugfx.clear()
		ugfx.set_default_font(ugfx.FONT_SMALL)
		w=ugfx.Container(0,0,ugfx.width(),ugfx.height())
		l=ugfx.Label(0,0,ugfx.width(),ugfx.height(),s.getvalue(),parent=w)
		w.show()
		raise(e)
	import onboard
	stm.mem8[0x40002850] = 0x9C
	import pyb
	pyb.hard_reset()