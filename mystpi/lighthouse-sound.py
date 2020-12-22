import time
import board
import neopixel
import signal
import sys
import random
from digitalio import DigitalInOut, Direction

# init 256 led neopixel panel
pixels=neopixel.NeoPixel(board.D18,256,auto_write=False)
cols=23 # 23 (of 32) columns are used
rows=8 # 8 rows

sound_trigger=DigitalInOut(board.D12)
sound_trigger.direction=Direction.OUTPUT
sound_trigger.value=True

# set up a cntrl-c handler to shut things down on exit
def signal_handler(sig,frame):
    off()
    sound_trigger=False
    sys.exit(0)
    
signal.signal(signal.SIGINT,signal_handler)

def foghorn():
    global sound_trigger
    sound_trigger.value=True
    time.sleep(0.2)
    sound_trigger.value=False
    time.sleep(0.2)
    sound_trigger.value=True

# turn everything off
def off():
    pixels.fill((0,0,0))
    pixels.show()

# to look at pixel order    
def sweep():
    for i in range(256):
        pixels[i]=(0,0,255)
        pixels.show()
        time.sleep(0.25)

# fill with a color        
def lh_fill(color):
    for i in range(cols*rows):
        pixels[i]=color
    pixels.show()

# round light pattern    
light_pat=[
    0,0,0,0,0,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,1,1,1,1,0,0,
    0,1,1,1,1,1,1,0,
    0,1,1,1,1,1,1,0,
    0,0,1,1,1,1,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,0,0,0,0,0
]

tree_pat=[
    0,0,1,0,0,0,0,0,
    0,0,1,0,0,0,0,0,
    0,0.5,1,0.5,0,0,0,0,
    0,1,1,1,0,0,0,0,
    0,1,1,1,0,0,0,0,
    0.5,1,1,1,0.5,0,0,0,
    1,1,1,1,1,0,0,0,
    0,0,1,0,0,0,0,0
]

# map x,y to pixel order (zig zag pattern)
def set_pix(x,y,color):
    x=cols-1-x
    k=x*8+(x%2)*y+(1-x%2)*(7-y)
    pixels[k]=color
    
# draw 8x8 pattern at x in a color    
def lh_pat(pat,sx,color,dcolor):
    for y in range(8):
        for x in range(8):
            rx=(x+sx)%cols
            if pat[y*8+x]>0:
                if pat[y*8+x]==1:
                    set_pix(rx,y,color)
                else:
                    set_pix(rx,y,dcolor)

def lh_sweep(pat,color,dcolor,bcolor,delay,two=None):
    for x in range(cols):
        pixels.fill(bcolor)
        #for i in range(10):
        #    set_pix(random.randrange(cols),random.randrange(8),(255,255,255))
        lh_pat(pat,x,color,dcolor)
        if two!=None:
            lh_pat(pat,(x+12)%cols,two[0],two[1])
        pixels.show()
        time.sleep(delay)

start=time.time()
horn=60
while True:
    #regular double white lighthouse pattern
    #lh_sweep(light_pat,(255,255,255),(40,40,40),(0,0,0),0.2,((255,255,255),(40,40,40)))
    #red and green xmas trees
    lh_sweep(tree_pat,(0,255,0),(0,40,0),(0,0,0),0.2,((255,0,0),(40,0,0)))
    if (time.time()-start)>horn:
        foghorn()
        start=time.time()


