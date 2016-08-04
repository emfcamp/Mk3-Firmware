from filesystem import *
from database import *
import pyb
import stm
import ugfx
import http_client
import socket
import network
import wifi
import gc
import onboard
import binascii

needs_wifi = True
period = 45 * 1000
needs_icon = True

i = 0
def tick(icon):
	global i
	i+=1

	icon.show()
	ugfx.set_default_font("c*")
	icon.area(0,0,icon.width(),icon.height(),0xFFFF)
	icon.text(0,0,str(i),0)

	bv = str(onboard.get_battery_voltage())
	uv = str(onboard.get_unreg_voltage())
	li = str(onboard.get_light())
	rssi = wifi.nic().get_rssi()
	
	aps = wifi.nic().list_aps()
	highest_rssi = -200
	nearestbssid = ""
	for a in aps:
		if (a['rssi'] > highest_rssi) and (a['rssi'] < 0):
			highest_rssi = a['rssi']
			nearestbssid = binascii.hexlify(a['bssid'])
	

	logfile = "log.txt"
	
	if not highest_rssi > -200:
		rssis = ","
		json={"vbat" : bv, "vunreg" : uv, "light" : li}
	else:
		rssis = str(highest_rssi) + "," + str(nearestbssid)
		json={"vbat" : bv, "vunreg" : uv, "light" : li, "rssi" : str(highest_rssi), "bssid" : str(nearestbssid)}

	if database_get("stats_upload", 0):
		#urlparams = "origin=PBADGE0&data=0bV" + str(uv) + "%5BPBADGE0%5D"
		
		try:
			if wifi.nic().is_connected():
				#with http_client.post('http://ukhas.net/api/upload', urlencoded=urlparams) as resp:
				with http_client.post('http://api.badge.emfcamp.org/api/barms', json=json) as resp:
					print(resp.text)
					#pass
		except OSError as e:
			print("Upload failed " + str(e))

	try:
		if not is_file(logfile):
			with open(logfile, "w") as f:
				f.write("vbat, vunreg, light, rssi, bssid \r\n")

		with open(logfile, "a") as f:			
			f.write(bv + ", " + uv + ", " + li + ", " + rssis + "\r\n")
	except OSError as e:
		print("Logging failed: " + str(e))
		return "Logging failed"


	return "Logged " + bv