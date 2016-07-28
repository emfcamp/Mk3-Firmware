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
from app import *
import filesystem

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

def connect():
    if not wifi.is_connected():
        with dialogs.WaitingMessage(text=wifi.connection_text(), title="TiLDA App Library") as message:
            wifi.connect()

def main_menu():
    clear()

    menu_items = [
        {"title": "Browse app library", "function": store},
        {"title": "Update apps and libs", "function": update},
        {"title": "Remove app", "function": remove}
    ]

    option = dialogs.prompt_option(menu_items, none_text="Exit", text="What do you want to do?", title="TiLDA App Library")

    if option:
        option["function"]()

def update():
    clear()
    connect()

    with dialogs.WaitingMessage(text="Downloading full list of library files", title="TiLDA App Library") as message:
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

        apps = get_local_apps()
        for i, app in enumerate(apps):
            message.text = "Checking app %s (%d/%d)" % (app, i + 1, len(apps))
            if app.fetch_api_information():
                files_to_update = []
                for file in app.files:
                    if file["hash"] != calculate_hash("%s/%s" % (app.folder_path, file["file"])):
                        files_to_update.append(file)

                base_text = message.text
                for j, file in enumerate(files_to_update):
                    message.text = base_text + "\nDownloading file %s (%d/%d)" % (file["file"], j + 1, len(files_to_update))
                    http_client.get(file["link"]).raise_for_status().download_to("%s/%s" % (app.folder_path, file["file"]))

    dialogs.notice("Everything is up-to-date")

    main_menu()

def store():
    global apps_by_category

    clear()
    connect()

    with dialogs.WaitingMessage(text="Fetching app library...", title="TiLDA App Library") as message:
        categories = get_public_app_categories()

    category = dialogs.prompt_option(categories, text="Please select a category", select_text="Browse", none_text="Back")
    print(category)
    if category:
        store_category(category)
    else:
        main_menu()

def store_category(category):
    clear()
    app = dialogs.prompt_option(get_public_apps(category), text="Please select an app", select_text="Details / Install", none_text="Back")
    if app:
        store_details(category, app)
    else:
        store()

def store_details(category, app):
    clear()
    print(category, app)
    with dialogs.WaitingMessage(text="Fetching app information...", title="TiLDA App Library") as message:
        app.fetch_api_information()

    clear()
    if dialogs.prompt_boolean(app.description, title = str(app), true_text = "Install", false_text="Back"):
        install(app)
        dialogs.notice("%s has been successfully installed" % (app))

    store_category(category)

def install(app):
    clear()
    connect()

    with dialogs.WaitingMessage(text="Installing %s" % (app), title="TiLDA App Library") as message:
        if not app.files:
            app.fetch_api_information()

        if not filesystem.is_dir(app.folder_path):
            os.mkdir(app.folder_path)

        files_to_update = []
        for file in app.files:
            if file["hash"] != calculate_hash("%s/%s" % (app.folder_path, file["file"])):
                files_to_update.append(file)

        base_text = message.text
        for j, file in enumerate(files_to_update):
            message.text = base_text + "\nDownloading file %s (%d/%d)" % (file["file"], j + 1, len(files_to_update))
            http_client.get(file["link"]).raise_for_status().download_to("%s/%s" % (app.folder_path, file["file"]))

def remove():
    clear()

    app = dialogs.prompt_option(get_local_apps(), title="TiLDA App Library", text="Please select an app to remove", select_text="Remove", none_text="Back")

    if app:
        clear()
        with dialogs.WaitingMessage(text="Removing %s\nPlease wait..." % app, title="TiLDA App Library") as message:
            for file in os.listdir(app.folder_path):
                os.remove(app.folder_path + "/" + file)
            os.remove(app.folder_path)
        remove()
    else:
        main_menu()

home_app = App("home")
if home_app.loadable:
    main_menu()
else:
    install(home_app)

pyb.hard_reset() # Bye!
