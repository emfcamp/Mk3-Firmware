import pyb
import math
import ugfx

btn_menu = pyb.Pin("BTN_MENU", pyb.Pin.IN)
btn_menu.init(pyb.Pin.IN, pull=pyb.Pin.PULL_UP)

ugfx.init()

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

while True:
    # Draw one frame
    ugfx.stream_start(minx, miny, maxx-minx, maxy-miny)
    for y in range(miny, maxy):
        h = (bally-y)*ii
        for x in range(minx, maxx):
            g=(ballx-x)*ii
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

    if (btn_menu.value() == 0):
        break
