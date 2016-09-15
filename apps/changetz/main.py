### Author: Thibault ML
### Description: Change timezone settings
### Category: Settings
### License: MIT
### Appname : Change Timezone

import pyb
import dialogs
import database
import ugfx

class Timezone:
	def __init__(self, name, value):
		self.name = name
		self.value = value

	def __str__(self):
		return self.name

timezone_list = [
	Timezone("UTC-12:00", -1200),
	Timezone("UTC-11:00", -1100),
	Timezone("UTC-10:00", -1000),
	Timezone("UTC-09:30", -0930),
	Timezone("UTC-09:00", -0900),
	Timezone("UTC-08:00", -0800),
	Timezone("UTC-07:00", -0700),
	Timezone("UTC-06:00", -0600),
	Timezone("UTC-05:00", -0500),
	Timezone("UTC-04:00", -0400),
	Timezone("UTC-03:30", -0330),
	Timezone("UTC-03:00", -0300),
	Timezone("UTC-02:00", -0200),
	Timezone("UTC-01:00", -0100),
	Timezone("UTC+00:00", +0000),
	Timezone("UTC+01:00", +0100),
	Timezone("UTC+02:00", +0200),
	Timezone("UTC+03:00", +0300),
	Timezone("UTC+03:30", +0330),
	Timezone("UTC+04:00", +0400),
	Timezone("UTC+04:30", +0430),
	Timezone("UTC+05:00", +0500),
	Timezone("UTC+05:30", +0530),
	Timezone("UTC+05:45", +0545),
	Timezone("UTC+06:00", +0600),
	Timezone("UTC+06:30", +0630),
	Timezone("UTC+07:00", +0700),
	Timezone("UTC+08:00", +0800),
	Timezone("UTC+08:30", +0830),
	Timezone("UTC+08:45", +0845),
	Timezone("UTC+09:00", +0900),
	Timezone("UTC+09:30", +0930),
	Timezone("UTC+10:00", +1000),
	Timezone("UTC+10:30", +1030),
	Timezone("UTC+11:00", +1100),
	Timezone("UTC+12:00", +1200),
	Timezone("UTC+12:45", +1245),
	Timezone("UTC+13:00", +1300),
	Timezone("UTC+14:00", +1400)
]

ugfx.init()

tz = dialogs.prompt_option(timezone_list, text="Select your timezone:", index=14)
with database.Database() as db:
	db.set("timezone", int(tz.value))
