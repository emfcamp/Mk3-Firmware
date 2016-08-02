### Author: EMF Badge team
### Description: Log stuff to memory
### Category: Comms
### License: MIT
### Appname : Logger
### Built-in: yes

import ugfx
from filesystem import *
from database import *
import pyb
import math
import buttons

def wait_for_exit():
	global chk_upload
	buttons.init()
	while True:
		pyb.wfi()
		if buttons.is_triggered("BTN_B"):
			break;
	
	database_set("stats_upload", chk_upload.checked())

wi = ugfx.width()
hi = ugfx.height()

ugfx.clear()

s = ugfx.Style()

s.set_enabled([ugfx.BLACK, ugfx.html_color(0xA66FB0), ugfx.html_color(0x5e5e5e), ugfx.RED])
s.set_background(ugfx.html_color(0xFFFFFF))

ugfx.set_default_style(s)

win_header = ugfx.Container(0,0,wi,33,style=s)
win_legend = ugfx.Container(0,hi-30,wi,30,style=s)


toplot = ['vbat','vunreg','light','rssi']
# scale  to fit on the y scale (range 0->150)
scale_m = [75,   75,   0.4,  1]
scale_c = [-255, -255, 0,    100]
colour =  [ugfx.RED, ugfx.ORANGE, ugfx.YELLOW, ugfx.BLUE]

buttons.disable_menu_reset()
timer = pyb.Timer(3)
timer.init(freq=10)
timer.callback(lambda t:ugfx.poll())

ugfx.set_default_font(ugfx.FONT_TITLE)
title = ugfx.Label(3,3,wi-10,45,"Log Viewer",parent=win_header)
ugfx.set_default_font(ugfx.FONT_SMALL)
chk_upload = ugfx.Checkbox(190,3,130,20,"M: Enable uplink",parent=win_header)
chk_upload.attach_input(ugfx.BTN_MENU,0)
if database_get("stats_upload", 0):
	chk_upload.checked(1)

win_header.show()
win_legend.show()

ugfx.set_default_font(ugfx.FONT_MEDIUM)
ugfx.set_default_style(s)

graph = ugfx.Graph(0,33,wi,hi-33-33,3,3)
graph.appearance(ugfx.Graph.STYLE_POINT, ugfx.Graph.POINT_NONE, 0, 0)
wi_g = wi - 3
graph.show()
ugfx.set_default_font(ugfx.FONT_SMALL)
win_zoom = ugfx.Container(1,33,92,25)
btnl = ugfx.Button(3,3,20,20,"<",parent=win_zoom)
btnr = ugfx.Button(68,3,20,20,">",parent=win_zoom)
l_cat = ugfx.Label(28,3,35,20,"1x",parent=win_zoom)
btnr.attach_input(ugfx.JOY_RIGHT,0)
btnl.attach_input(ugfx.JOY_LEFT,0)
win_zoom.show()

scaling = int((hi-33-33-30)/2)

lines = 0
names = []
seek = -1
if not is_file("log.txt"):
	ugfx.text(20,100,"Log file not found",0)
	wait_for_exit()
	pyb.hard_reset()


#open the file and see how long it is
with open("log.txt","r") as f:
	l = f.readline()
	lines += 1;
	names = l.split(",")
	while len(f.readline()):
		lines += 1;


cl = 0
x_index = 0

names=[n.strip() for n in names]

xscale = int(max(math.floor(wi/lines),1))

zoom = [1, 2, 4, 8, 16]
lines_z = []
for z in zoom:
	lines_z.append(lines-(z*wi_g))
seeks = [0, 0, 0, 0, 0]

with open("log.txt","r") as f:		
	#now we know how long the file is, look for the index of the start of the plotting area
	l=f.readline()  #ignore the title
	ra = range(1,len(zoom))
	while True:
		seek = f.tell()
		l=f.readline()
		if len(l) == 0:
			break
		for r in ra:
			if (cl == lines_z[r]):
				seeks[r] = seek
		if (cl >= lines-wi_g):
			seeks[0] = seek
			break
		cl += 1	


		
def plot(start,file_step,xscale):
	global names
	global toplot
	global scale_m
	global scale_c
	global graph
	print("drawing from index " + str(start) + "  in steps of " + str(file_step) + "   " + str(xscale))
	seek = start
	with open("log.txt","r") as f:
		#plot each line
		col = 0
		for n in names:
			if n in toplot:
				f.seek(seek)
				graph.appearance(ugfx.Graph.STYLE_LINE, ugfx.Graph.LINE_SOLID, 3, colour[ toplot.index(n) ])			
				x_index = 0
				m = scale_m[ toplot.index(n) ]
				c = scale_c[ toplot.index(n) ]
				new_series = 1
				while True:
					rs = file_step
					while rs:
						l=f.readline()
						rs -= 1
					if len(l) == 0:
						break
					s = l.strip().split(",")
					if len(s) > col:
						try:
							data_y = int((float(s[col])*m)+c)
							graph.plot(x_index, data_y, new_series)
							new_series = 0
						except ValueError:
							pass
					x_index += xscale
			col += 1

#plot the legend
x = 0
i=0
ugfx.set_default_font(ugfx.FONT_SMALL)
for p in toplot:
	ugfx.Label(x+13,0,50,25,p,parent=win_legend)
	win_legend.thickline(x,13,x+10,13,colour[ i ],3,1,)
	i += 1
	x += 75
	
plot(seeks[0],zoom[0],xscale)

plot_index = 0
buttons.init()
while True:
	pyb.wfi()
	inc = 0
	if buttons.is_triggered("JOY_RIGHT"):
		inc = -1
	if buttons.is_triggered("JOY_LEFT"):
		inc = 1
	if buttons.is_triggered("BTN_B"):
		break;
		
	if not inc == 0:
		inc += plot_index
		if inc < 0:
			pass
		elif inc >= len(zoom):
			pass
		elif seeks[0] == 0: ## dont allow zoom out if we dont have enough data
			pass
		else:
			plot_index = inc
			graph.destroy()
			graph = ugfx.Graph(0,33,wi,hi-33-33,3,3)
			graph.appearance(ugfx.Graph.STYLE_POINT, ugfx.Graph.POINT_NONE, 0, 0)
			graph.show()
			win_zoom.hide(); win_zoom.show()
			if plot_index == 0:
				l_cat.text("1x")
			else:
				l_cat.text("1/" + str(zoom[plot_index])+"x")
			plot(seeks[plot_index],zoom[plot_index],1)

			
database_set("stats_upload", chk_upload.checked())		

