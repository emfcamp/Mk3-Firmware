# borrowed from https://github.com/micropython/micropython/blob/master/esp8266/scripts/ntptime.py
import socket
import pyb
import network

# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600

host = "pool.ntp.org"

def getntptime():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    import struct
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA

def settime():
    import time
    from pyb import RTC
    t = getntptime()
    tm = time.localtime(t)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    rtc = RTC()
    rtc.init()
    rtc.datetime(tm)

nic = network.CC3100()
nic.connect("<ssid>","<psk>")
while (not nic.is_connected()):
    nic.update()
    pyb.delay(100)


# set the RTC using time from ntp
settime()
# print out RTC datetime
pyb.RTC().datetime()

