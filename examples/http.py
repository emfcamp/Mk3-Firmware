import wifi
from http_client import get

wifi.connect()

try:
	if wifi.nic().is_connected():
		ip = get('http://httpbin.org/ip').raise_for_status().json()["origin"]
		print("My public IP is %s" %(ip))
except OSError as e:
		print("Query failed " + str(e))
