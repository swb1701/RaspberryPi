import board
import neopixel
import time
from datetime import datetime

pixels=neopixel.NeoPixel(board.D18,16,auto_write=False,pixel_order=neopixel.RGB)

def clear(): #clear all pixels
    pixels.fill((0,0,0))

def set_pixel(x,y,color): #set pixel in a color (x=0-4 is windows left to right, y=0-4 from bottom to top)
    num=y*4+(y%2)*(3-x)+(1-y%2)*x #wire zig zags up the house
    pixels[num]=color

def show_time():
    clear()
    now=datetime.now() #get the time
    digits=now.strftime("%H%M") #format in digits
    d=[0,0,0,0]
    for i in range(4):
        d[i]=int(digits[i]) #convert each digit to an integer
    for x in range(4):
        for y in range(4):
            if (d[x]&(2**y)!=0): #if the appropriate bit is set
                set_pixel(x,y,(255,255,255)) #turn the light on
    pixels.show()

pixels.fill((255,0,0))
pixels.show()
time.sleep(0.5)
pixels.fill((0,255,0))
pixels.show()
time.sleep(0.5)
pixels.fill((0,0,255))
pixels.show()
time.sleep(0.5)

    
while(True):    
    show_time()
    time.sleep(1)

