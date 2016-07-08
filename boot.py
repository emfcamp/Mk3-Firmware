import pyb
import json
import os

entrypoint = "bootstrap.py"
if "apps" in os.listdir():
    apps = os.listdir("apps")
    if "home" in apps:
        entrypoint = "apps/home/main.py"
    elif "updater" in apps:
        entrypoint = "apps/updater/main.py"

pyb.main(entrypoint)





