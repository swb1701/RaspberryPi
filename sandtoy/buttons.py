#!/usr/bin/python

import time
import subprocess

try:
    import RPi.GPIO as gpio
except ImportError:
    exit("This library requires the RPi.GPIO module\nInstall with: sudo pip install RPi.GPIO")

BUTTON_MODE  = 19  # Cycle between modes
BUTTON_RESET = 25  # Restart current mode
BUTTONS      = [BUTTON_RESET, BUTTON_MODE]
PROGRAMS     = ["demo1-snow", "demo2-hourglass", "demo3-logo","demo","wheel","nl-logo","maze","maze2"]
FLAGS        = ["--led-rgb-sequence=rbg", "--led-brightness=100","--led-rows=64","--led-cols=64","-D 7"]
MODE         = 0
PROCESS      = None
lastpress    = 0

def handle_button(pin):
    global MODE,lastpress
    now=time.time()
    if ((now-lastpress)>1): #one second min between presses
        lastpress=now
        # Ignore 'rising' events.  For some reason we're
        # still getting them despite only asking for 'falling'.
        if gpio.input(pin) == 0:
            if pin == BUTTON_MODE:         # Mode button pressed?
                MODE += 1                  # Advance to next mode
                if MODE >= len(PROGRAMS):  # Wrap around to start if needed
                    MODE = 0
            launch()

def launch():
    global PROCESS
    if PROCESS is not None:
        PROCESS.terminate()
	while PROCESS.poll() is not None:
            continue     # Wait for process to terminate
        time.sleep(0.5) # No, really, wait (seemingly necessary kludge)
    PROCESS = subprocess.Popen(["./" + PROGRAMS[MODE]] + FLAGS)

# GPIO init
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
for button in BUTTONS:
    gpio.setup(button, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.add_event_detect(button, gpio.FALLING,
      callback=handle_button, bouncetime=200)

launch()

while True:
    time.sleep(1.0)
