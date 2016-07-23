import pyb, json, os, micropython

micropython.alloc_emergency_exception_buf(100)

m = "bootstrap.py"
if "apps" in os.listdir():
	apps = os.listdir("apps")
	if "home" in apps:
		m = "apps/home/main.py"
	elif "updater" in apps:
		m = "apps/updater/main.py"

pyb.main(m)
