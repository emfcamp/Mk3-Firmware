import pyb
import json
import os

btn_menu = pyb.Pin("BTN_MENU", pyb.Pin.IN)
btn_menu.init(pyb.Pin.IN, pull=pyb.Pin.PULL_UP)

def config():
    if "config.json" in os.listdir():
        with open("config.json") as f:
            return json.loads(f.read())
    return {}

path = "bootstrap.py"
if "apps" in os.listdir():
    apps = [a.split(".py")[0] for a in os.listdir("apps") if ".py" in a and a[0] != "."]
    if apps:
        app = config()["current"];
        if btn_menu.value() == 0 or app not in apps:
            app = "selector" 
        if app not in apps:
            app = apps[0]

        path = "apps/%s.py" % (app)
    
pyb.main(path)


