### author: emf badge team
### description: updates and installs apps. To publish apps use https://badge.emfcamp.org
### license: MIT
### depends: wifi, http_client, badge

import ugfx
import os
import pyb
import http_client
import wifi
import hashlib
import binascii
import buttons, dialogs

API_URL = "http://badge.marekventur.com/mock_api"
LIB_URL = "http://badge.marekventur.com/lib"

ugfx.init()

def clear():
    ugfx.clear(ugfx.html_color(0x7c1143))

def main_menu():
    clear()
    option = dialogs.prompt_option(["Update widgets and libs", "Browse widget store", "Remove widget"], none_text="Exit", text="What do you want to do?", title="TiLDA Widget Store")

    if not option:
        return

    if "Update" in option:
        update()
    elif "Browse" in option:
        store()
    else:
        remove()

def update():
    clear()
    with dialogs.WaitingMessage(text=wifi.connection_text(), title="TiLDA Widget Updater") as message:
        wifi.connect()

    with dialogs.WaitingMessage(text="Please wait while we're updating your libs", title="TiLDA Widget Updater") as message:
        master = http_client.get("http://api.badge.emfcamp.org/firmware/master.json").raise_for_status().json()
        print(master)

    main_menu()

def store():
    clear()
    with dialogs.WaitingMessage(text="Store", title="TiLDA Widget Store") as message:
        pyb.delay(2000)
    install("foo", "bar")

def install(user, app):
    with dialogs.WaitingMessage(text="Install", title="TiLDA Widget Store") as message:
        pyb.delay(2000)
    main_menu()

def remove():
    with dialogs.WaitingMessage(text="Removing", title="TiLDA Widget Store") as message:
        pyb.delay(2000)
    main_menu()

update()
pyb.hard_reset() # Bye!




#info = None
#with http_client.get(API_URL + "/info.json") as response:
#    response.raise_for_status() # Make sure it's a 2xx status
#    info = response.json()
#
#def calculate_hash(filename):
#    try:
#        with open(filename, "rb") as file:
#            sha256 = hashlib.sha256()
#            for line in file:
#                sha256.update(line)
#            return str(binascii.hexlify(sha256.digest()), "utf8")
#    except OSError as e:
#        return "OSERR"
#
#message("Checking your current list of libraries")
#
#libs_to_update = []
#for lib, expected_hash in info["libs"].items():
#    if expected_hash != calculate_hash("lib/%s" % (lib)):
#        libs_to_update.append(lib)
#
#if libs_to_update:
#    for i, lib in enumerate(libs_to_update):
#        print(i, lib, LIB_URL + "/" + lib)
#        message("Downloading lib/%s (%d/%d)" % (lib, i, len(libs_to_update)))
#        with http_client.get(LIB_URL + "/" + lib) as response:
#            print(LIB_URL + "/" + lib)
#            response.raise_for_status() # Make sure it's a 2xx status
#            print(response.headers)
#            print("lib/%s.new" % (lib))
#            # ToDo: Make sure folder exists
#            response.download_to("lib/%s.new" % (lib))
#            print("done")
#            # ToDo: Switch out old file with new one
#
## ToDo: Finish this once downloads are more reliable
## ToDo: Apps
#message("Done")
