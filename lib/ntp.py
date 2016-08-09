### Description: Update the badge's time via NTP
### License: MIT

import database
import pyb
import socket


# (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
NTP_DELTA = 3155673600
NTP_HOST = "pool.ntp.org"


def get_NTP_time():
	NTP_QUERY = bytearray(48)
	NTP_QUERY[0] = 0x1b
	addr = socket.getaddrinfo(NTP_HOST, 123)[0][-1]
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	res = s.sendto(NTP_QUERY, addr)
	msg = s.recv(48)
	s.close()
	import struct
	val = struct.unpack("!I", msg[40:44])[0]
	return val - NTP_DELTA


def set_NTP_time():
	import time
	from pyb import RTC
	print("Setting time from NTP")

	tz = 0
	with database.Database() as db:
		tz = db.get("timezone", 0)

	t = get_NTP_time()
	tz_minutes = int(abs(tz) % 100) * (1 if tz >= 0 else -1)
	tz_hours = int(tz / 100)
	t += (tz_hours * 3600) + (tz_minutes * 60)

	tm = time.localtime(t)
	tm = tm[0:3] + (0,) + tm[3:6] + (0,)

	rtc = RTC()
	rtc.init()
	rtc.datetime(tm)
