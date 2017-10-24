#!/usr/bin/python
import subprocess as sp
import time
import os
from pirDetect import *
import sys

video = ["omxplayer", "filename", "-o", "both", "--win", "0 0 1600 900", "--aspect-mode", "fill", "--no-osd", "--orientation" ,"0","--vol", "-600"]
scareFile = "/home/pi/Video.mp4"
print(scareFile)

def onMotion(currState):
    if currState:
        video[1] = scareFile
        subVideo = sp.Popen(video)
        while subVideo.poll() is None:
            time.sleep(.1)


def showImage():
    os.system("sudo fbi -a -T 1 -d /dev/fb0 -noverbose -once /home/pi/Start.png")


showImage()
objDetect = detector(7)
objDetect.subscribe(onMotion)
objDetect.start()
os.system("sudo killall -9 fbi")
