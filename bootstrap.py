import network
import pyb
import usocket
import machine
import os
import json
import ugfx

def download(path, target):
    host = "badge.marekventur.com"
    ai = usocket.getaddrinfo(host, 80) # ToDo: Change to 443 once we have https
    sock = usocket.socket()
    sock.connect(ai[0][4]) # .wrap_socket(sock) # enable HTTPS
    sock.send('GET /%s HTTP/1.0\r\nHost: %s\r\nConnection: close\r\n\r\n' % (path, host))

    # write to disk
    with open(target, 'wb') as f:
        state = 1
        hbuf = b"";
        remaining = None;
        while True:
            buf = sock.recv(1024)
            if state == 1: # Status
                nl = buf.find(b"\n")
                if nl > -1:
                    hbuf += buf[:nl - 1]
                    status = hbuf.split(b' ')[1]
                    if status != b"200":
                        raise Exception("Invalid status " + str(status))

                    state = 2
                    hbuf = b"";
                    buf = buf[nl + 1:]
                else:
                    hbuf += buf

            if state == 2: # Headers
                hbuf += buf
                nl = hbuf.find(b"\n")
                while nl > -1:
                    if nl < 2:
                        if remaining == None:
                            raise Exception("No Content-Length")
                        buf = hbuf[2:]
                        hbuf = None
                        state = 3
                        break

                    header = hbuf[:nl - 1].decode("utf8").split(':', 3)
                    if header[0] == "Content-Length":
                        remaining = int(header[1].strip())

                    hbuf = hbuf[nl + 1:]
                    nl = hbuf.find(b"\n")

            if state == 3: # Content
                f.write(buf)
                remaining -= len(buf)
                if remaining < 1:
                    break

            pyb.delay(50)

    sock.close()

ugfx.init()
ugfx.area(0, 0, ugfx.width(), ugfx.height(), ugfx.BLACK)
ugfx.text(0, 0, "Downloading Tilda software", ugfx.RED)
ugfx.text(0, 30, "Should this not work, try again by", ugfx.WHITE)
ugfx.text(0, 50, "pressing the reset button at the back", ugfx.WHITE)
ugfx.text(0, 100, "Please wait...", ugfx.WHITE)

def message(lines):
    y = 150;
    ugfx.area(0, y, ugfx.width(), ugfx.height() - y, 0)
    for line in lines:
        ugfx.text(0, y, line, ugfx.WHITE)
        y += 20

def mkdir(d):
    try:
        os.mkdir(d)
    except OSError as e:
        print(e)


mkdir("apps")
mkdir("apps/updater")
mkdir("lib")

w = {}
try:
    if "wifi.json" in os.listdir():
        with open("wifi.json") as f:
            w = json.loads(f.read())
except ValueError as e:
    print(e)

if not ("ssid" in w and "pw" in w):
    message(["Couldn't find a valid wifi.json :(", "See https://badge.emf.camp", "for more information"])
    while True: pass

wifi_ssid = w["ssid"]
wifi_pw = w["pw"]

message(["Connecting to wifi " + wifi_ssid, "Update wifi.json if this is incorrect"])
nic = network.CC3100()
nic.connect(wifi_ssid, wifi_pw)
while not nic.is_connected():
    nic.update()
    pyb.delay(100)

try:
    message(["Downloading updater.py (1/3)"])
    download("/apps/updater/main.py", "apps/updater/main.py")
    message(["Downloading http_client.py (2/3)"])
    download("/lib/http_client.py", "lib/http_client.py")
    message(["Downloading boot.py (3/3)"])
    download("/boot.py", "boot.py")
finally:
    os.sync()
machine.reset()

