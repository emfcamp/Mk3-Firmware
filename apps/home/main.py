### Author: EMF Badge team
### Description: Main app
### Category: Other
### License: MIT
### Appname: Home
### Built-in: hide


import os
import json

if 'main.json' in os.listdir():
	m = None
	try:
		with open('main.json', 'r') as f:
			main_dict = json.loads(f.read())
			m = main_dict['main']
			if not main_dict.get('perm', False):
				os.remove('main.json')				
	except Exception as e:
		print(e)	
		
	if m:		
		import run_app
		run_app.run_app(m)


execfile("apps/home/home.py")
