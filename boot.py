# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal
# this is a special version for EMF
#pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
#pyb.usb_mode('CDC+HID') # act as a serial device and a mouse

import pyb, json, os, micropython

micropython.alloc_emergency_exception_buf(100)

m = "bootstrap.py"
if "main.py" in os.listdir():
    m = "main.py"
elif "apps" in os.listdir():
	apps = os.listdir("apps")
	if ("home" in apps) and ("main.py" in os.listdir("apps/home")):
		m = "apps/home/main.py"
	elif ("app_library" in apps) and ("main.py" in os.listdir("apps/app_library")):
		m = "apps/app_library/main.py"
pyb.main(m)
