#!/usr/bin/python
import subprocess as sp
import time
import os
import datetime
from pirDetect import *
import sys

takeVideo=True #whether to film and playback the user
syncAudio=False #whether to only play audio when synced (omxplayer loses sync if video capture is at full resolution)
video = ["omxplayer", "filename", "-o", "alsa:hw:1,0", "--win", "0 0 1600 900", "--aspect-mode", "fill", "--no-osd", "--orientation" ,"0","--vol", "-600"]
record = ["raspivid", "-o", "filename", "-n", "-t", "15000", "-rot","270","-w","960"]
current = 3
videoFiles = ["/home/pi/Video.mp4","/home/pi/Video2.mp4","/home/pi/Video3.mp4","/home/pi/GentEyes.mp4","/home/pi/GirlEyes.mp4","/home/pi/LadyEyes.mp4"]
stillFiles = ["/home/pi/Start.png","/home/pi/Start2.png","/home/pi/Start3.png","/home/pi/Start.png","/home/pi/Start3.png","/home/pi/Start2.png"]

def getFileName():
    return "/home/pi/recordings/" + datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")

def subProcWait(params):
        sub = sp.Popen(params)
        while sub.poll() is None:
            time.sleep(.1)

def onMotion(currState):
    global current
    if currState:
        if takeVideo and current<3:
            autoFileName = getFileName()  # Get a time stamped file name
            record[2] = autoFileName
            subRecord = sp.Popen(record)  # Start recording to capture their fright
            if syncAudio:
                video[3]="both" #taking video causes audio to lose sync, don't play it
        else:
            if syncAudio:
                video[3]="alsa:hw:1,0" #we can keep audio sync, so play audio
        video[1] = videoFiles[current]
        subProcWait(video)  # Play the video to scare them
        if takeVideo and current<3:
            video[1] = autoFileName
            subProcWait(video)  # Play back the video we just recorded
        os.system("sudo killall -9 fbi")
        current=current+1
        if (current>5):
            current=0
        showImage(current)
        

def showImage(num):
    os.system("sudo fbi -a -T 1 -d /dev/fb0 -noverbose -once "+stillFiles[num])

showImage(current)
objDetect = detector(7)
objDetect.subscribe(onMotion)
objDetect.start()
os.system("sudo killall -9 fbi")
