import wifi
from http_client import *

wifi.connect()

ip = get('http://httpbin.org/ip').raise_for_status().json()["origin"]
print("My public IP is %s" %(ip))

