import time
import board
import neopixel
import signal
import sys

pixels=neopixel.NeoPixel(board.D18,256,auto_write=False)
cols=23
rows=8

def signal_handler(sig,frame):
    off()
    sys.exit(0)

def off():
    pixels.fill((0,0,0))
    pixels.show()
    
def sweep():
    for i in range(256):
        pixels[i]=(0,0,255)
        pixels.show()
        time.sleep(0.25)

def lh_fill(color):
    for i in range(cols*rows):
        pixels[i]=color
    pixels.show()

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

def set_pix(x,y,color):
    x=cols-1-x
    k=x*8+(x%2)*y+(1-x%2)*(7-y)
    pixels[k]=color

def lh_pat(pat,sx,color):
    for y in range(8):
        for x in range(8):
            rx=(x+sx)%cols
            if pat[y*8+x]==1:
                set_pix(rx,y,color)

def lh_sweep(pat,color,delay):
    for x in range(cols):
        pixels.fill((0,0,0))
        lh_pat(pat,x,color)
        pixels.show()
        time.sleep(delay)
        
def lh_sweep2(pat,color,delay):
    for x in range(cols):
        pixels.fill((0,0,0))
        lh_pat(pat,x,color)
        lh_pat(pat,(x+12)%cols,color)
        pixels.show()
        time.sleep(delay)

def test():    
  for y in range(rows):
    for x in range(cols):
      set_pix(x,y,(0,0,255))
      pixels.show()
      time.sleep(0.02)

signal.signal(signal.SIGINT,signal_handler)
    
#pixels.fill((255,255,255))
#pixels.show()
#time.sleep(10)
#off()
#lh_pat(light_pat,0,(0,0,255))
while True:
    lh_sweep2(light_pat,(255,255,255),0.2)
#time.sleep(10)
#test()
off()

