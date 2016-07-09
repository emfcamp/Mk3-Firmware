### author: emf badge team
### description: updates and installs apps. To manage your list of apps use https://badge.emf.camp
### license: MIT
### depends: wifi, http_client, badge

import ugfx
import os
import pyb
import http_client
import wifi
import hashlib
import binascii

API_URL = "http://badge.marekventur.com/mock_api"
LIB_URL = "http://badge.marekventur.com/lib"

ugfx.init()
ugfx.area(0, 0, ugfx.width(), ugfx.height(), ugfx.BLACK)
ugfx.text(0, 0, "TiLDA App Updater", ugfx.RED)

def message(*args):
    y = 40;
    ugfx.area(0, y, ugfx.width(), ugfx.height() - y, 0)
    for line in args:
        ugfx.text(0, y, line, ugfx.WHITE)
        y += 20

message("Connecting to %s..." % (wifi.ssid()), "Please update wifi.json if this", "is incorrect")
wifi.connect()
message("Downloading your list of apps...")

info = None
with http_client.get(API_URL + "/info.json") as response:
    response.raise_for_status() # Make sure it's a 2xx status
    info = response.json()

def calculate_hash(filename):
    try:
        with open(filename, "rb") as file:
            sha256 = hashlib.sha256()
            for line in file:
                sha256.update(line)
            return str(binascii.hexlify(sha256.digest()), "utf8")
    except OSError as e:
        return "OSERR"

message("Checking your current list of libraries")

libs_to_update = []
for lib, expected_hash in info["libs"].items():
    if expected_hash != calculate_hash("lib/%s" % (lib)):
        libs_to_update.append(lib)

if libs_to_update:
    for i, lib in enumerate(libs_to_update):
        print(i, lib, LIB_URL + "/" + lib)
        message("Downloading lib/%s (%d/%d)" % (lib, i, len(libs_to_update)))
        with http_client.get(LIB_URL + "/" + lib) as response:
            print(LIB_URL + "/" + lib)
            response.raise_for_status() # Make sure it's a 2xx status
            print(response.headers)
            print("lib/%s.new" % (lib))
            # ToDo: Make sure folder exists
            response.download_to("lib/%s.new" % (lib))
            print("done")
            # ToDo: Switch out old file with new one

# ToDo: Finish this once downloads are more reliable
# ToDo: Apps
message("Done")
