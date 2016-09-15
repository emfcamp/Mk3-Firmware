# TiLDA Badge Bootstrap script
# Automatically downloads the app library to the badge via wifi
import pyb
import machine
import os
import ugfx
import hashlib
import binascii
import uio
import sys
import buttons
import dialogs
import wifi
from http_client import get

def calculate_hash(filename):
    try:
        with open(filename, "rb") as file:
            sha256 = hashlib.sha256()
            buf = file.read(128)
            while len(buf) > 0:
                sha256.update(buf)
                buf = file.read(128)
        return str(binascii.hexlify(sha256.digest()), "utf8")
    except:
        return "ERR"

def download(url, target, expected_hash):
    while True:
        get(url).raise_for_status().download_to(target)
        if calculate_hash(target) == expected_hash:
            break

ugfx.init()
buttons.init()

wifi.connect(
    wait=True,
    show_wait_message=True,
    prompt_on_fail=True,
    dialog_title='TiLDA Setup'
)

addendum = "\n\n\n\nIf stalled for 2 minutes please press the reset button on the back"
with dialogs.WaitingMessage(text="Please wait" + addendum, title="Downloading TiLDA software") as message:

    success = False
    failure_counter = 0
    URL = "http://api.badge.emfcamp.org/firmware"

    while not success:
        for d in ["apps", "apps/app_library", "lib"]:
            try:
                os.remove(d) # Sometimes FS corruption leads to files instead of folders
            except OSError as e:
                pass
            try:
                os.mkdir(d)
            except OSError as e:
                print(e)

        try:
            message.text = "Downloading list of libraries" + addendum
            master = get(URL + "/master.json").raise_for_status().json()
            libs_to_update = []
            for i, (lib, expected_hash) in enumerate(master["lib"].items()):
                message.text ="Downloading library: %s (%d/%d)%s" % (lib, i + 1, len(master["lib"]), addendum)
                download(URL + "/master/lib/%s" % lib, "lib/%s" % lib, expected_hash)

            message.text = "Downloading app library" + addendum
            download(URL + "/master/apps/app_library/main.py", "apps/app_library/main.py", master["apps"]["app_library"]["main.py"])
            success = True

	except Exception as e:
            error_string = uio.StringIO()
            sys.print_exception(e, error_string)
            error_string = error_string.getvalue()

            failure_counter += 1
            print("Error:")
            print(error_string)

            if failure_counter > 5:
                message.text = "Something went wrong for the 5th time, giving up :(\nError:\n%s" % error_string
                while True:
                    pyb.wfi()

                    message.text = "Something went wrong, trying again..."
                    pyb.delay(1000)

    os.sync()
    machine.reset()
