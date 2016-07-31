### Author: EMF Badge team
### Description: Log stuff to memory
### Category: Comms
### License: MIT
### Appname : Logger
### Built-in: yes

import ugfx
from filesystem import *
import pyb
import math

wi = ugfx.width()
hi = ugfx.height()

ugfx.clear()

s = ugfx.Style()
s.set_focus(ugfx.RED)
s.set_enabled([ugfx.BLACK, ugfx.html_color(0xA66FB0), ugfx.html_color(0x5e5e5e), ugfx.RED])
s.set_background(ugfx.html_color(0xFFFFFF))

ugfx.set_default_style(s)

win_header = ugfx.Container(0,0,wi,33)
win_legend = ugfx.Container(0,hi-30,wi,30)


toplot = ['vbat','light','rssi']
# scale  to fit on the y scale (range 0->150)
scale_m = [75,   1,  1]
scale_c = [-255, 0,  0]
colour =  [ugfx.RED, ugfx.GREEN, ugfx.BLUE]


ugfx.set_default_font(ugfx.FONT_TITLE)
title = ugfx.Label(3,3,wi-10,45,"Log Viewer",parent=win_header)
win_header.show()
win_legend.show()

ugfx.set_default_font(ugfx.FONT_MEDIUM)
ugfx.set_default_style(s)

graph = ugfx.Graph(0,33,wi,hi-33-33,30,30)
graph.appearance(ugfx.Graph.STYLE_POINT, ugfx.Graph.POINT_NONE, 0, 0)
wi_g = wi - 30

scaling = int((hi-33-33-30)/2)

lines = 0
names = []
seek = -1
if not is_file("log.txt"):
	ugfx.text(20,100,"Log file not found",0)
	pyb.wfi()


#open the file and see how long it is
with open("log.txt","r") as f:
	l = f.readline()
	lines += 1;
	names = l.split(",")
	while len(f.readline()):
		lines += 1;


cl = 0
x_index = 0
graph.show()

xscale = int(max(math.floor(wi/lines),1))

with open("log.txt","r") as f:		
	#now we know how long the file is, look for the index of the start of the plotting area
	l=f.readline()  #ignore the title
	while True:
		seek = f.tell()
		l=f.readline()
		if len(l) == 0:
			break				
		if (cl >= lines-wi_g):
			break
		cl += 1	
	
	#plot each line
	col = 0
	for n in names:
		if n in toplot:
			f.seek(seek)
			graph.appearance(ugfx.Graph.STYLE_LINE, ugfx.Graph.LINE_SOLID, 1, colour[ toplot.index(n) ])			
			x_index = 0
			m = scale_m[ toplot.index(n) ]
			c = scale_c[ toplot.index(n) ]
			while True:
				l=f.readline()
				if len(l) == 0:
					break
				s = l.strip().split(",")
				if len(s) > col:
					try:
						data_y = int((float(s[col])*m)+c)
						graph.plot(x_index, data_y)
					except ValueError:
						pass
				x_index += xscale
		col += 1

#plot the legend
x = 0
for p in toplot:
	ugfx.Label(x+13,0,50,25,p,parent=win_legend)
	win_legend.line(x,13,x+10,13,colour[ toplot.index(p) ])
	x += 75
						
while True:
	pyb.wfi()