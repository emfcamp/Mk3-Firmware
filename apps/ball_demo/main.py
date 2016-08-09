### Author: Joel Bodenmann aka Tectu <joel@unormal.org>, Andrew Hannam aka inmarket
### Description: A python port of the UGFX ball demo
### Category: Examples
### License: BSD

# Copyright (c) 2012, 2013, Joel Bodenmann aka Tectu <joel@unormal.org>
# Copyright (c) 2012, 2013, Andrew Hannam aka inmarket
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the <organization> nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pyb
import ugfx
import buttons

ugfx.init()
buttons.init()

BALLCOLOR1 =    ugfx.RED
BALLCOLOR2 =    ugfx.YELLOW
WALLCOLOR =     ugfx.GREEN
BACKCOLOR =     ugfx.BLUE
FLOORCOLOR =    ugfx.PURPLE
SHADOWALPHA =   (255-255*0.2)

width = ugfx.width()
height = ugfx.height()

radius=height/5+height%2+1 # The ball radius
ii = 1.0/radius            # radius as easy math
floor=height/5-1           # floor position
spin=0.0                   # current spin angle on the ball
spinspeed=0.1              # current spin speed of the ball
ballx=width/2              # ball x position (relative to the ball center)
bally=height/4             # ball y position (relative to the ball center)
dx=.01*width               # motion in the x axis
dy=0.0                     # motion in the y axis
ballcx = 12*radius/5       # ball x diameter including the shadow
ballcy = 21*radius/10      # ball y diameter including the shadow

# The clipping window for this frame.
minx = miny = 0
maxx = width
maxy = height

def invsqrt(x):
    return x**-1/2

while not buttons.is_triggered("BTN_MENU"):
    # Draw one frame
    ugfx.stream_start(minx, miny, maxx-minx, maxy-miny)
    for x in range(minx, maxx):
        g = (ballx-x)*ii
        for y in range(miny, maxy):
            h = (bally-y)*ii
            f=-.3*g+.954*h
            if g*g < 1-h*h:
                # The inside of the ball
                if ((int((9-spin+(.954*g+.3*h)*invsqrt(1-f*f)))+int((2+f*2))&1)):
                    colour = BALLCOLOR1
                else:
                    colour = BALLCOLOR2
            else:
                # The background (walls and floor)
                if y > height-floor:
                    if x < height-y or height-y > width-x:
                        colour = WALLCOLOR
                    else:
                        colour = FLOORCOLOR
                elif x<floor or x>width-floor:
                    colour = WALLCOLOR
                else:
                    colour = BACKCOLOR

                # The ball shadow is darker
                #if (g*(g+.4)+h*(h+.1) < 1)
                #    colour = gdispBlendColor(colour, Black, SHADOWALPHA);

            ugfx.stream_color(colour) # pixel to the LCD
    ugfx.stream_stop()

    # Calculate the new frame size (note this is a drawing optimisation only)
    minx = ballx - radius
    miny = bally - radius
    maxx = minx + ballcx
    maxy = miny + ballcy

    if dx > 0:
        maxx += dx
    else:
        minx += dx

    if dy > 0:
        maxy += dy
    else:
        miny += dy

    if minx < 0:
        minx = 0

    if maxx > width:
        maxx = width

    if miny < 0:
        miny = 0

    if maxy > height:
        maxy = height

    minx = int(minx);
    miny = int(miny);
    maxx = int(maxx);
    maxy = int(maxy);

    # Motion
    spin += spinspeed
    ballx += dx
    bally += dy

    if ballx < radius or ballx > width-radius:
        spinspeed = -spinspeed
        dx = -dx

    if bally > height-1.75*floor:
        dy = -.04*height
    else:
        dy = dy+.002*height;

pyb.hard_reset()
