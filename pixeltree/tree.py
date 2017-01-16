#!/usr/bin/python

#96 Pixel Tree Demo
# Scott Bennett, 1/17
# Based on Pi WS2812 Library by Jeremy Garff
# Some Routines by Tony DiCola (tony@tonydicola.com)
import signal
import sys
import time

from neopixel import *

#Ring Pixel Counts
rings=[32, 24, 16, 12, 8, 1]
#Offset of Rings
offset=[0, 32, 56, 72, 84, 92]


# LED strip configuration:
LED_COUNT      = 93      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

#Clear strip on shut down
def signal_handler(signal, frame):
        print("Shutting tree down")
        clear(strip)
        sys.exit(0)

#Register handler        
signal.signal(signal.SIGINT, signal_handler)

#Quickly clear the strip
def clear(strip):
        for i in range(strip.numPixels()):
                strip.setPixelColor(i,Color(0,0,0))
        strip.show()

def grow(strip, color, wait_ms=50):
        clear(strip)
        time.sleep(wait_ms/1000.0)
        for i in range(len(rings)):
                for j in range(rings[i]):
                        strip.setPixelColor(j+offset[i],color)
                strip.show()
                time.sleep(wait_ms/1000.0)
                
def sweep(strip, color, wait_ms=50):
        clear(strip)
        time.sleep(wait_ms/1000.0)
        for i in range(len(rings)):
                for j in range(rings[i]):
                        strip.setPixelColor(j+offset[i],color)
                strip.show()
                time.sleep(wait_ms/1000.0)
                for j in range(rings[i]):
                        strip.setPixelColor(j+offset[i],Color(0,0,0))
                        
def alt(strip, color1, color2, wait_ms=250):
        clear(strip)
        time.sleep(wait_ms/1000.0)
        for k in range(50):
                for i in range(len(rings)):
                        for j in range(rings[i]):
                                if ((i+k)%2==0):
                                        strip.setPixelColor(j+offset[i],color1)
                                else:
                                        strip.setPixelColor(j+offset[i],color2)
                strip.show()
                time.sleep(wait_ms/1000.0)

def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)


if __name__ == '__main__':
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	strip.begin()

	print ('Press Ctrl-C to quit.')
	while True:
                alt(strip,Color(255,0,0),Color(0,255,0))
                for i in range(10):
                        grow(strip,Color(255,0,0),25)
                for i in range(10):
                        grow(strip,Color(0,255,0),25)
                for i in range(10):
                        sweep(strip,Color(255,0,0))
                for i in range(10):
                        sweep(strip,Color(0,255,0))
		colorWipe(strip, Color(255, 0, 0))  # Red wipe
		colorWipe(strip, Color(0, 255, 0))  # Blue wipe
		colorWipe(strip, Color(0, 0, 255))  # Green wipe
		# Theater chase animations.
		theaterChase(strip, Color(127, 127, 127))  # White theater chase
		theaterChase(strip, Color(127,   0,   0))  # Red theater chase
		theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
		# Rainbow animations.
		rainbow(strip)
		rainbowCycle(strip)
		theaterChaseRainbow(strip)
