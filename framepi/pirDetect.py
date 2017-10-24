#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os

class detector(object):
        def __init__(self, sensor):
                self.callBacks = []
                self.sensor = sensor
                self.currState = False
                self.prevState = False

                GPIO.setmode(GPIO.BOARD)
                GPIO.setup(self.sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        def read(self):
                self.prevState = self.currState
                self.currState = GPIO.input(self.sensor)

        def printState(self):
                print( "GPIO pin {0} is {1}".format(self.sensor, "HIGH" if self.currState else "LOW"))

        def subscribe(self, callBack):
                self.callBacks.append(callBack)

        def callBack(self, state):
                for fn in self.callBacks:
                        fn(state)

        def start(self):
                try:
                        self.read()
                        self.printState()
                        while True:
                                 self.read()
                                 if self.currState != self.prevState:
                                         self.printState()
                                         self.callBack(self.currState)
                                 time.sleep(.1)

                except (KeyboardInterrupt, SystemExit):
	#Since fbi doesn't restore the console correctly when the application is exited we do a little clean up.
						os.system('stty sane')
