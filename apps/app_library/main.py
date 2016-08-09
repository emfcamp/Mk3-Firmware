### author: emf badge team
### description: updates and installs apps. To publish apps use https://badge.emfcamp.org
### license: MIT

import ugfx
import os
import pyb
import http_client
import wifi
import buttons
import dialogs
from app import *
import filesystem

TEMP_FILE = ".temp_download"

ugfx.init()

### HELPER FUNCTIONS ###

def clear():
    ugfx.clear(ugfx.html_color(0x7c1143))

def download(url, target, expected_hash):
    if filesystem.calculate_hash(target) == expected_hash:
        return
    count = 0

    while filesystem.calculate_hash(TEMP_FILE) != expected_hash:
        count += 1
        if count > 5:
            os.remove(TEMP_FILE)
            raise OSError("Aborting download of %s after 5 unsuccessful attempts" % url)
        http_client.get(url).raise_for_status().download_to(TEMP_FILE)

    os.rename(TEMP_FILE, target)

def download_list(items, message_dialog):
    for i, item in enumerate(items):
        message_dialog.text = "Downloading %s (%d/%d)" % (item["title"], i + 1, len(items))
        http_client.get(item["url"]).raise_for_status().download_to(item["target"])

def download_app(app, message_dialog):
    files_to_update = []
    for file in app.files:
        file_path = "%s/%s" % (app.folder_path, file["file"])
        if file["hash"] != filesystem.calculate_hash(file_path):
            data = {
                "url": file["link"],
                "target": file_path,
                "expected_hash": file["hash"],
                "title": app.folder_name + "/" + file["file"]
            }

            if file["file"] == "main.py": # Make sure the main.py is the last file we load
                files_to_update.append(data)
            else:
                files_to_update.insert(0, data)

    download_list(files_to_update, message_dialog)

def connect():
    if not wifi.is_connected():
        with dialogs.WaitingMessage(text=wifi.connection_text(), title="TiLDA App Library") as message:
            wifi.connect()

### VIEWS ###

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
        master = http_client.get("http://api.badge.emfcamp.org/firmware/master-lib.json").raise_for_status().json()
        libs_to_update = []
        for lib, expected_hash in master.items():
            if expected_hash != filesystem.calculate_hash("lib/" + lib):
                libs_to_update.append({
                    "url": "http://api.badge.emfcamp.org/firmware/master/lib/" + lib,
                    "target": "lib/" + lib,
                    "expected_hash": expected_hash,
                    "title": lib
                })
        download_list(libs_to_update, message)

        apps = get_local_apps()
        for i, app in enumerate(apps):
            message.text = "Updating app %s" % app
            if app.fetch_api_information():
                download_app(app, message)

    dialogs.notice("Everything is up-to-date")

    main_menu()

def store():
    global apps_by_category

    clear()
    connect()

    with dialogs.WaitingMessage(text="Fetching app library...", title="TiLDA App Library") as message:
        categories = get_public_app_categories()

    category = dialogs.prompt_option(categories, text="Please select a category", select_text="Browse", none_text="Back")
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
    empty_local_app_cache()
    with dialogs.WaitingMessage(text="Fetching app information...", title="TiLDA App Library") as message:
        app.fetch_api_information()

    clear()
    if dialogs.prompt_boolean(app.description, title = str(app), true_text = "Install", false_text="Back"):
        install(app)
        dialogs.notice("%s has been successfully installed" % app)

    store_category(category)

def install(app):
    clear()
    connect()

    with dialogs.WaitingMessage(text="Installing %s" % app, title="TiLDA App Library") as message:
        if not app.files:
            app.fetch_api_information()

        if not filesystem.is_dir(app.folder_path):
            os.mkdir(app.folder_path)

        download_app(app, message)

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

if App("home").loadable:
    main_menu()
else:
    for app_name in ["sponsors", "changename", "snake", "rnalexander~changefi", "home"]:
        install(App(app_name))
    pyb.hard_reset()
