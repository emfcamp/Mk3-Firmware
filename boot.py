# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal
# this is a special version for EMF
#pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
#pyb.usb_mode('CDC+HID') # act as a serial device and a mouse

import pyb, json, os, micropython

micropython.alloc_emergency_exception_buf(100)

m = "bootstrap.py"
if "apps" in os.listdir():
	apps = os.listdir("apps")
	if "home" in apps:
		m = "apps/home/main.py"
	elif "widget_store" in apps:
		m = "apps/widget_store/main.py"

pyb.main(m)
