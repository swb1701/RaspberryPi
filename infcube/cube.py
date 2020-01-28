import board
import neopixel
import time
from datetime import datetime
from signal import signal, SIGINT
from sys import exit

total=12*12
pixels=neopixel.NeoPixel(board.D18,total,auto_write=False)

def handler(signal,frame):
    print("Goodbye...")
    pixels.fill((0,0,0))
    pixels.show()
    exit(0)
    
signal(SIGINT,handler)

for i in range(total):
    pixels[i]=(0,0,255)
    pixels.show()
    time.sleep(0.1)  

while True:
    pixels.fill((50,0,0))
    pixels.show()
    time.sleep(1.0)
    pixels.fill((0,50,0))
    pixels.show()
    time.sleep(1.0)
    pixels.fill((0,0,50))
    pixels.show()
    time.sleep(1.0)


