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
        _nic = nic = network.CC3100()
    return _nic

def connection_details():
    data = {}
    try:
        if "wifi.json" in os.listdir():
            with open("wifi.json") as f:
                data = json.loads(f.read())
    except ValueError as e:
        print(e)

    if not ("ssid" in data and "pw" in data):
        raise OSError("Couldn't find a valid wifi.json. See https://badge.emf.camp for more information")

    return data

def ssid():
    return connection_details()["ssid"]

def connect(wait = True):
    if nic().is_connected:
        return
    details = connection_details()
    nic().connect(details["ssid"], details["pw"])
    if wait:
        wait_for_connection()

def wait_for_connection():
    while not nic().is_connected():
        nic().update()
        pyb.delay(100)

def connection_text():
    return "Connecting to wifi '%s'. If this doesn't work, please check your wifi.json. More information: badge.emfcamp.org/TiLDA_MK3/wifi" % (ssid())
