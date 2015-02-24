#!/usr/bin/python
#
#Foosball Scoring Controller
#Scott Bennett 2/15
#
import RPi.GPIO as GPIO
import time
import os
import random
import Queue
import requests
import json
from Adafruit_LED_Backpack import SevenSegment
from Adafruit_MAX9744 import Adafruit_MAX9744
from subprocess import call, check_output

# Create display instance on default I2C address (0x70) and bus number.
display = SevenSegment.SevenSegment()
display.begin()
display.clear()
display.write_display()
# Adafruit MAX9744 amplifier on I2C at 0x4f
amp = Adafruit_MAX9744()
amp.set_volume(30)

streams="Scott's Foosball Table:i"
tokens="secrettoken"
score1=0
score2=0
name1="Player1"
name2="Player2"
cmdQueue=Queue.Queue()

requests.packages.urllib3.disable_warnings()

#need start game button (record time of each shot for game stats)

goals=["airhorn.wav","buzzer.wav","boxing.wav","cheering.wav","glass.wav","whoop.wav"]

def send(msg):
    msg['time']=time.time()
    msgjson=json.dumps(msg)
    requests.post('https://temporacloud.com/connection/clientSend', data={'streams':streams,'tokens':tokens,'message':msgjson},verify=False)

def displayScore(s1,s2):
    s11=int(s1/10)
    s12=s1%10
    s21=int(s2/10)
    s22=s2%10
    display.clear()
    if (s11>0):
        display.set_digit(0,s11)
    display.set_digit(1,s12)
    if (s21>0):
        display.set_digit(2,s21)
    display.set_digit(3,s22)
    display.write_display()

def setVolume(v):
    amp.set_volume(v)

def startGame():
    global score1,score2
    score1=0
    score2=0
    send({'type':'start','name1':name1,'name2':name2})
    updateScore()
    speak("starting game")

def updateScore():
    global score1,score2
    send({'type':'score','score1':score1,'score2':score2})
    displayScore(score1,score2)
    if (score1==10 or score2==10):
        gameOver()

def gameOver():
    if (score1==10):
        send({'type':'win','winner':name1})
        speak(name1+" wins!")
    elif (score2==10):
        send({'type':'win','winner':name2})
        speak(name2+" wins!")
    time.sleep(10)
    startGame()

GPIO.setmode(GPIO.BCM)

def callback17(channel):
    global score1,name1
    score1=score1+1
    updateScore()
    goalsound(name1+" score sound for point "+str(score1))
    speak(name1+" scores")
    return

def callback18(channel):
    global score2,name2
    score2=score2+1
    updateScore()
    goalsound(name2+" score sound for point "+str(score2))
    speak(name2+" scores")
    return

def callback22(channel):
    speak("listening")
    cmdQueue.put({'type':'recog'})
    return

def goalsound(comment):
    play(goals[random.randint(0,len(goals)-1)],comment)
    return

def play(sound,comment):
    cmdQueue.put({'type':'play','file':sound,'comment':comment})

def speak(text):
    cmdQueue.put({'type':'tts','text':text})

def recog():
    global score1,score2
    display.clear()
    display.write_display()
    result=check_output("/home/pi/recog.sh",shell=True)
    displayScore(score1,score2)
    result=result.translate(None,'"')
    result=result.strip()
    print("Heard:"+result)
    call("tts what i heard was",shell=True)
    call("aplay /dev/shm/sample.wav",shell=True)
    runSpeechCmd(result)

def runSpeechCmd(text):
    global name1,name2
    text=text.lower()
    if (text.find(" vs ")>-1):
        pos=text.find(" vs ")
        name1=text[:pos].capitalize()
        name2=text[pos+4:].capitalize()
        send({'type':'names','name1':name1,'name2':name2})
        speak("Game is now "+name1+" vs "+name2)
    elif (text=="start game"):
        startGame()
        

GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22,GPIO.IN, pull_up_down=GPIO.PUD_UP)
#ts1=time.time()
#ts2=time.time()
GPIO.add_event_detect(17,GPIO.FALLING,callback=callback17,bouncetime=800)
GPIO.add_event_detect(18,GPIO.FALLING,callback=callback18,bouncetime=800)
GPIO.add_event_detect(22,GPIO.FALLING,callback=callback22,bouncetime=800)

startGame()

i=0
while True:
    while not cmdQueue.empty():
        cmd=cmdQueue.get()
        if (cmd['type']=='tts'):
            print("Speaking "+cmd['text'])
            call("tts "+cmd['text'],shell=True)
        elif (cmd['type']=='play'):
            print("Playing "+cmd['comment'])
            call("aplay sounds/"+cmd['file'],shell=True)
        elif (cmd['type']=='recog'):
            print("Speech Recognition")
            recog()
    time.sleep(1)

amp.cleanup()
