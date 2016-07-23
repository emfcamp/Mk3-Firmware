import ugfx
from filesystem import *
import pyb

wi = ugfx.width()
hi = ugfx.height()

win_header = ugfx.Container(0,0,wi,30)



ugfx.set_default_font("D*")
title = ugfx.Label(3,3,wi-10,45,"Log Viewer",parent=win_header)

s = ugfx.Style()
s.set_focus(ugfx.RED)

ugfx.set_default_font("c*")
ugfx.set_default_style(s)

graph = ugfx.Graph(0,33,wi,hi-33-33,30,30)
graph.set_style(ugfx.Graph.STYLE_POINT, ugfx.Graph.POINT_NONE, 0, 0)


scaling = int((hi-33-33-30)/2)

lines = 0
if not is_file("log.txt"):
	ugfx.text(20,100,":(",0)
else:

	with open("log.txt","r") as f:
		while len(f.readline()):
			lines += 1;
	f.seek(0)
	cl = 0
	index = 0
	graph.show()
	with open("log.txt","r") as f:		
		while True:
			l=f.readline()
			if len(l) == 0:
				break;
			cl += 1		
			if (cl > lines-wi):
				s = l.strip().split(",")
				if len(s) > 0:
					try:
						data_y = int((float(s[0])-3)*scaling)
						index += 1
						graph.plot(index, data_y)
					except ValueError:
						data_y = 0


while True:
	pyb.wfi()