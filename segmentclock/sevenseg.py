# Servo2.py
# Two servo motors driven by PCA9685 chip
from smbus import SMBus
from PCA9685 import PWM
import time
import json
import os.path
import sys
import getopt

fPWM = 50
i2c_address = 0x40 # (standard) adapt to your module
channel = 0 # adapt to your wiring
a = 8.5 # adapt to your servo
b = 2 # adapt to your servo
tune=False
clock=False
stow=False
pwm=[0,0]

def setup():
 global pwm
 bus = SMBus(1) # Raspberry Pi revision 2
 pwm[0] = PWM(bus, i2c_address)
 pwm[0].setFreq(fPWM)
 pwm[1] = PWM(bus, i2c_address+1)
 pwm[1].setFreq(fPWM)
 
def setDirection(channel,direction):
 duty = a / 180 * direction + b
 if (channel>15):
  pwm[1].setDuty(channel-16, duty)
 else:
  pwm[0].setDuty(channel, duty)
 if tune:
  print "direction =", direction, "-> duty =", duty
 #time.sleep(1) # allow to settle

def showDigit(offset,num):
 global last
 digit=digits[num]
 mask=0x40
 for i in range(7):
  if (mask&digit)!=0:
   if (last[offset+i]!=1):
    setDirection(offset+i,limits[str(offset+i)+'-up'])
    last[offset+i]=1
  else:
   if (last[offset+i]!=0):
    setDirection(offset+i,limits[str(offset+i)+'-down'])
    last[offset+i]=0
  mask=mask>>1

usage="Usage: python sevenseg.py [-h] [-t] [-c] [-s]"

try:
  opts, args = getopt.getopt(sys.argv[1:],"thcs")
except getopt.GetoptError:
  print(usage)
  sys.exit(2)

for opt, arg in opts:
 if opt=='-h':
  print(usage)
  sys.exit()
 elif opt=='-t':
  tune=True
 elif opt=='-c':
  clock=True
 elif opt=='-s':
  stow=True

setup()

digits=[0x77,0x12,0x5d,0x5b,0x3a,0x6b,0x6f,0x52,0x7f,0x7b,0x00]
#-1=not init,0=down,1=up
last=[-1]*32

limits={}

if (os.path.isfile("servos.json")):
 with open('servos.json') as file:
  limits=json.load(file)

if tune:  
 while True:
  servo='q'
  try:
   servo=raw_input("Servo #>")
  except:
   pass
  if (servo==''):
   break
  servo=int(servo)
  angle=0
  key=str(servo)+'-up'
  if (key in limits):
   angle=limits[key]
   setDirection(servo,angle)
  while True:
   step='0'
   try:
    step=raw_input("Step (or 'up' or 'down')>")
   except:
    break
   if (step==''):
    break
   elif (step=='up'):
    limits[str(servo)+'-up']=angle
    print(limits)
    with open('servos.json','w') as file:
     file.write(json.dumps(limits))
   elif (step=='down'):
    limits[str(servo)+'-down']=angle
    print(limits)
    with open('servos.json','w') as file:
     file.write(json.dumps(limits))
   else:
    step=int(step)
    angle+=step
    setDirection(servo,angle)
 with open('servos.json','w') as file:
  file.write(json.dumps(limits))
elif clock:
  while True:
   t=time.strftime("%I%M")
   z=ord('0')
   if (ord(t[0])-z)==0:
    showDigit(0,10)
   else:
    showDigit(0,ord(t[0])-z)
   showDigit(7,ord(t[1])-z)
   showDigit(16,ord(t[2])-z)
   showDigit(23,ord(t[3])-z)
   time.sleep(1)
elif stow:
 showDigit(0,10)
 showDigit(7,10)
 showDigit(16,10)
 showDigit(23,10)
else:
  for i in range(10000):
   n1=int(i/1000)
   n2=int((i-n1*1000)/100)
   n3=int((i-n1*1000-n2*100)/10)
   n4=int(i-n1*1000-n2*100-n3*10)
   showDigit(0,n1)
   showDigit(7,n2)
   showDigit(16,n3)
   showDigit(23,n4)
   time.sleep(0.5)
   
