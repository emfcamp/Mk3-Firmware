wifi_ssid = "VM9425583"
wifi_pw = "n3tXpVhvwjsp"

import network
import pyb
import usocket
import machine
import uos
import json

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


l = pyb.UGFX()
l.area(0,0,l.get_width(),l.get_height(),0)
l.text("Downloading Tilda software", 0, 00, pyb.UGFX.RED)
l.text("Should this not work, try again by", 0, 30, pyb.UGFX.WHITE)
l.text("pressing the reset button at the back", 0, 50, pyb.UGFX.WHITE)
l.text("Please wait...", 0, 100, pyb.UGFX.WHITE)

def message(lines):
    y = 150;
    l.area(0, y, l.get_width(), l.get_height() - y, 0)
    for line in lines:
        l.text(line, 0, y, pyb.UGFX.WHITE)
        y += 20

def mkdirp(path):
    try:
        uos.mkdir(path)
    except OSError:
        pass

mkdirp("apps")
mkdirp("lib")

message(["Connecting to wifi " + wifi_ssid, "Update bootstrap.py if this is incorrect"])
nic = network.CC3100()
nic.connect(wifi_ssid, wifi_pw)
while (not nic.is_connected()):
    nic.update()
    pyb.delay(100)

with open("wifi.json", 'wb') as f:
    f.write(json.dumps({"ssid":wifi_ssid, "pw":wifi_pw}))

message(["Downloading updater.py (1/3)"])
download("/apps/updater.py", "apps/updater.py")
message(["Downloading http_client.py (2/3)"])
download("/lib/http_client.py", "lib/http_client.py")
message(["Downloading boot.py (3/3)"])
download("/bootstrap/boot.py", "boot.py")
uos.sync()
machine.reset()
