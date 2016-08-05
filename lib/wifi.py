### Author: EMF Badge team
### Description: Handles connecting to a wifi access point based on a valid wifi.json file
### License: MIT

import network
import os
import json
import pyb

_nic = None

def nic():
    global _nic
    if not _nic:
        _nic = network.CC3100()
    return _nic

def create_default_config():
    with open("wifi.json", "wt") as file:
        file.write(json.dumps({"ssid": "emfcamp-insecure"}))
        file.flush()
    os.sync()

def connection_details():
    data = {}
    try:
        if "wifi.json" in os.listdir():
            with open("wifi.json") as f:
                data = json.loads(f.read())
    except ValueError as e:
        print(e)

    if "ssid" not in data:
        raise OSError("Couldn't find a valid wifi.json. See https://badge.emf.camp for more information")

    return data

def ssid():
    return connection_details()["ssid"]

def connect(wait = True, timeout = 10):
    if nic().is_connected():
        return
    details = connection_details()

    if "pw" in details and details["pw"]:
        if wait:
            nic().connect(details["ssid"], details["pw"], timeout=timeout)
            wait_for_connection()
        else:
            nic().connect(details["ssid"], details["pw"], timeout=None)
    else:
        if wait:
            nic().connect(details["ssid"], timeout=timeout)
            wait_for_connection()
        else:
            nic().connect(details["ssid"], timeout=None)


def wait_for_connection():
    while not nic().is_connected():
        nic().update()
        pyb.delay(100)

def is_connected():
    return nic().is_connected()

def connection_text():
    return "Connecting to wifi '%s'. If this doesn't work, please check your wifi.json. More information: badge.emfcamp.org/TiLDA_MK3/wifi" % (ssid())
