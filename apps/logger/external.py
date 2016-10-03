from filesystem import is_file
from database import database_get
import stm
import http_client
import wifi
import onboard
import binascii

needs_wifi = True
period = 120 * 1000

def tick():
	bv = str(onboard.get_battery_voltage())
	uv = str(onboard.get_unreg_voltage())
	li = str(onboard.get_light())
	wifi.nic().get_rssi()

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
		r1 = stm.mem32[0x1FFF7590]
		r1 |= (stm.mem32[0x1FFF7594]<<32)
		r1 |= (stm.mem32[0x1FFF7598]<<64)
		json={"vbat" : bv, "vunreg" : uv, "light" : li, "rssi" : str(highest_rssi), "bssid" : str(nearestbssid), "uuid":"%x" % r1}

	if database_get("stats_upload"):
		try:
			if wifi.nic().is_connected():
				with http_client.post('http://api.badge.emfcamp.org/api/barms', json=json):
					pass
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
