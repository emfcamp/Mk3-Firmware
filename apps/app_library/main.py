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
import buttons
import dialogs
import gc

ugfx.init()

def clear():
    ugfx.clear(ugfx.html_color(0x7c1143))

def calculate_hash(filename):
    try:
        with open(filename, "rb") as file:
            sha256 = hashlib.sha256()
            buf = file.read(128)
            while len(buf) > 0:
                sha256.update(buf)
                buf = file.read(128)
                gc.collect()
            return str(binascii.hexlify(sha256.digest()), "utf8")
    except OSError as e:
        return "OSERR"

def main_menu():
    clear()
    option = dialogs.prompt_option(["Update apps and libs", "Browse app library", "Remove app"], none_text="Exit", text="What do you want to do?", title="TiLDA App Library")

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
    with dialogs.WaitingMessage(text=wifi.connection_text(), title="TiLDA App Library") as message:
        wifi.connect()

        message.text="Downloading full list of library files"
        master = http_client.get("http://api.badge.emfcamp.org/firmware/master.json").raise_for_status().json()
        libs_to_update = []
        for lib, expected_hash in master["lib"].items():
            actual_hash = calculate_hash("lib/" + lib)
            if expected_hash != actual_hash:
                libs_to_update.append(lib)

        for i, lib in enumerate(libs_to_update):
            message.text = "Downloading %s (%d/%d)" % (lib, i + 1, len(libs_to_update))
            http_client.get("http://api.badge.emfcamp.org/firmware/master/lib/" + lib).raise_for_status().download_to("lib/" + lib)

        message.text="Checking list of local apps"
        apps = os.listdir("apps")
        for i, foldername in enumerate(apps):
            [username, app] = foldername.split("-", 1) if (foldername.find("-") > -1) else ["emf", foldername]
            message.text = "Checking app %s from author %s (%d/%d)" % (app, username, i + 1, len(apps))
            with http_client.get("http://api.badge.emfcamp.org/api/app/%s/%s" % (username, app)) as response:
                if response.status == 404:
                    continue # App not found in app library, skipping
                response.raise_for_status() # Deal with all other errors correctly
                data = response.json()

                files_to_update = []
                for file in data["files"]:
                    if file["hash"] != calculate_hash("apps/%s/%s" % (foldername, file["file"])):
                        files_to_update.append(file)

                base_text = message.text
                for j, file in enumerate(files_to_update):
                    message.text = base_text + "\nDownloading file %s (%d/%d)" % (file["file"], j + 1, len(files_to_update))
                    http_client.get(file["link"]).raise_for_status().download_to("apps/%s/%s" % (foldername, file["file"]))

    dialogs.notice("Everything is up-to-date")

    main_menu()

apps_by_category = None
def store():
    global apps_by_category

    clear()
    if not apps_by_category:
        with dialogs.WaitingMessage(text=wifi.connection_text(), title="TiLDA App Library") as message:
            wifi.connect()

            message.text="Fetching app library..."
            apps_by_category = http_client.get("http://api.badge.emfcamp.org/api/apps").raise_for_status().json()

    category = dialogs.prompt_option(list(apps_by_category.keys()), text="Please select a category", select_text="Browse", none_text="Back")
    if category:
        store_category(category)
    else:
        main_menu()

def store_category(category):
    clear()

    apps = apps_by_category[category]

    for app in apps:
        app["title"] = "%s by %s" % (app["name"], app["user"])

    app = dialogs.prompt_option(apps, text="Please select an app", select_text="Details / Install", none_text="Back")

    if app:
        store_details(category, app)
    else:
        store()

def store_details(category, app):
    clear()
    data = None
    with dialogs.WaitingMessage(text="Fetching app information...", title="TiLDA App Library") as message:
        data = http_client.get(app["link"]).raise_for_status().json()

    clear()
    title = app["name"] + " by " + app["user"];
    if dialogs.prompt_boolean(app["description"], title = title, true_text = "Install", false_text="Back"):
        install(data = data)
        dialogs.notice("%s has been successfully installed" % (title))

    store_category(category)

def install(link = None, data = None):
    clear()

    if not apps_by_category:
        with dialogs.WaitingMessage(text=wifi.connection_text(), title="TiLDA App Library") as message:
            wifi.connect()

    with dialogs.WaitingMessage(text="Fetching app information...", title="TiLDA App Library") as message:
        if link:
            data = http_client.get(link).raise_for_status().json()

        message.text = "Installing..."
        foldername = data["user"] + "-" + data["name"]

        if foldername.lower() not in map(str.lower, os.listdir("apps")):
            os.mkdir("apps/" + foldername)

        files_to_update = []
        for file in data["files"]:
            if file["hash"] != calculate_hash("apps/%s/%s" % (foldername, file["file"])):
                files_to_update.append(file)

        base_text = message.text
        for j, file in enumerate(files_to_update):
            message.text = base_text + "\nDownloading file %s (%d/%d)" % (file["file"], j + 1, len(files_to_update))
            http_client.get(file["link"]).raise_for_status().download_to("apps/%s/%s" % (foldername, file["file"]))

def remove():
    clear()
    apps = []
    with dialogs.WaitingMessage(text="Scanning your apps folder...", title="TiLDA App Library") as message:
        for foldername in os.listdir("apps"):
            app = { "user": "emf", "name": foldername, "foldername": foldername }
            if foldername.find("-") > -1:
                [app["user"], app["name"]] = foldername.split("-", 1)
            app["title"] = "%s by %s" % (app["name"], app["user"])
            apps.append(app)

    app = dialogs.prompt_option(apps, title="TiLDA App Library", text="Please select an app to remove", select_text="Remove", none_text="Back")

    if app:
        clear()
        folder_path = "apps/" + app["foldername"]
        with dialogs.WaitingMessage(text="Removing %s\nPlease wait..." % (app["title"]), title="TiLDA App Library") as message:
            for file in os.listdir(folder_path):
                print(folder_path + "/" + file)
                os.remove(folder_path + "/" + file)
            os.remove(folder_path)
        remove()
    else:
        main_menu()

if ("home" not in os.listdir("apps")) or ("main.py" not in os.listdir("apps/home")):
    install(link="http://api.badge.emfcamp.org/api/app/emf/home")
else:
    store()
pyb.hard_reset() # Bye!
