import serial
import math
import os
import time

#Simple Brecknell Talking Scale (Using Embedded Pi Zero) -- Scott Bennett 1/19

ser=serial.Serial('/dev/ttyUSB0',2400)

last_reading=None

while True:
    same=False
    sameStart=0
    lastline=None
    line=None
    while True:
        millis=int(round(time.time()*1000))
        line=ser.read_until('\r')
        if not same and lastline==line:
            same=True
            sameStart=millis
        if same and lastline==line and (millis-sameStart)>500:
            break
        if lastline!=line:
            same=False
        lastline=line
    bval=bytearray(line)
    val=''.join(format(x,'02x') for x in bval)
    mode=val[4]
    sign=val[5]
    num=val[10:20]
    speak=None
    if (mode=='b'):
        lbs=bval[5]*10+bval[6]
        ounces=bval[7]*10+bval[8]+0.1*bval[9]
        if lbs==0:
            speak=str(ounces)+" ounces"
        else:
            speak=str(lbs)+" pounds "+str(ounces)+" ounces"
    elif mode=='c':
        grams=bval[5]*math.pow(10,4)+bval[6]*math.pow(10,3)+bval[7]*math.pow(10,2)+bval[8]*10+bval[9]
        speak=str(int(grams))+" grams"
    elif mode=='a':
        kg=bval[6]*10+bval[7]+0.1*bval[8]+0.01*bval[9]
        speak=str(kg)+" kilograms"
    if (speak!=last_reading):
        print(speak)
        os.system("espeak -ven-us+m7 '"+speak+"'")
        last_reading=speak

                
    

