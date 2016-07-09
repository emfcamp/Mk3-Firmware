### Author: EMF Badge team
### Description: Handles connecting to a wifi access point based on a valid wifi.json file
### License: MIT

import network
import os
import json
import pyb

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

def connect():
    details = connection_details()
    nic = network.CC3100()
    nic.connect(details["ssid"], details["pw"])
    while (not nic.is_connected()):
        nic.update()
        pyb.delay(100)
