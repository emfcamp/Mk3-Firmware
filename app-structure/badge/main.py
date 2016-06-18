import network
import socket
import pyb

lcd=pyb.UGFX()
btn = lcd.text("My name is", 40, 40, pyb.UGFX.RED)