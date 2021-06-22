#flap control for 8-digits with 2 MCP23017s, single-threaded
import time
import board
import digitalio
import busio
import sys
import datetime
import pytz
from adafruit_mcp230xx.mcp23017 import MCP23017
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
 
# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)

mcp = MCP23017(i2c)  #All steppers will be driven by MCP23017
mcp2 = MCP23017(i2c,address=0x21)

for i in range(16):
    p=mcp.get_pin(i)
    p.switch_to_output()
    p=mcp2.get_pin(i)
    p.switch_to_output()

chandigit={5:0,6:1,13:2,19:3,22:4,27:5,17:6,4:7}

def home(channel):
    d=chandigit[channel]
    if digit_step[d]==-1:
        moving.append(d)
    digit_step[d]=0

digit_step=[-1,-1,-1,-1,-1,-1,-1,-1]    
#digit_offset=[13,39,13,0,0,0,0,0]
digit_offset=[26+4,26,26+4,26+8,13+4,39+4,13,0+4]
digit_mask=[0xFF0FFFFF,0xFFF0FFFF,0x0FFFFFFF,0xF0FFFFFF,0xFFFFFFF0,0xFFFFFF0F,0xFFFFF0FF,0xFFFF0FFF]
#digit_mask=[0xF0FF,0xFFF0,0xFF0F,0x0FFF] #for turning a motor off
digit_mask2=[0X00F00000,0x000F0000,0xF0000000,0x0F000000,0x0000000F,0x000000F0,0x00000F00,0x0000F000]
#digit_mask2=[0x0F00,0x000F,0x00F0,0xF000] #for detecting which motor is on
target=[-1,-1,-1,-1,-1,-1,-1,-1]

#Wiring
#Digit: I2C,IN1-IN4 Home
#1: 20,4-7 5
#2: 20,0-3 6
#3: 20,12-15 13
#4: 20,8-11 19
#5: 21,0-3 22
#6: 21,4-7 27
#7: 21,8-11 17
#8: 21,12-15 4

#set up the home interrupts
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(5,GPIO.FALLING,callback=home,bouncetime=200)
GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(6,GPIO.FALLING,callback=home,bouncetime=200)
GPIO.setup(13,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(13,GPIO.FALLING,callback=home,bouncetime=200)
GPIO.setup(19,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(19,GPIO.FALLING,callback=home,bouncetime=200)
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(22,GPIO.FALLING,callback=home,bouncetime=200)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(27,GPIO.FALLING,callback=home,bouncetime=200)
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(17,GPIO.FALLING,callback=home,bouncetime=200)
GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(4,GPIO.FALLING,callback=home,bouncetime=200)

symbols=" ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:.,"

#set a target word
def set_target(word):
    word=word.ljust(8,' ')
    for i in range(8):
        loc=symbols.find(word[i])
        pos=int((loc/40)*512)
        target[i]=digit_offset[i]+pos

#check after each microstep whether a digit goal was achieved        
def check(delay):
    global mask,moving
    #time.sleep(delay)
    #return
    t0=time.time()
    #print(f"steps={digit_step}")
    for i in moving:#range(8):
        #if digit_step[i]>-1:# and mask&digit_mask2[i]!=0: #if we are moving the digit
        if digit_step[i]==target[i]*8: #if the target digit stop moving
            mask=digit_mask[i]&mask #mask off the digit
            moving.remove(i)
            #print(f"steps={digit_step}")
        else:
            digit_step[i]=digit_step[i]+1 #otherwise increment
    if mask==0: #if nothing is moving then signal to exit
        return(True)
    rem=delay-(time.time()-t0) #calculate remaining delay needed (if any)
    if rem>0:
        time.sleep(delay)
        
def fh(delay,steps):
    for i in range(steps):
        mcp.gpio=(mask>>16)&0x8888
        mcp2.gpio=mask&0x8888
        if check(delay):
            return
        mcp.gpio=(mask>>16)&0xCCCC
        mcp2.gpio=mask&0xCCCC
        if check(delay):
            return
        mcp.gpio=(mask>>16)&0x4444
        mcp2.gpio=mask&0x4444
        if check(delay):
            return
        mcp.gpio=(mask>>16)&0x6666
        mcp2.gpio=mask&0x6666
        if check(delay):
            return
        mcp.gpio=(mask>>16)&0x2222
        mcp2.gpio=mask&0x2222
        if check(delay):
            return
        mcp.gpio=(mask>>16)&0x3333
        mcp2.gpio=mask&0x3333
        if check(delay):
            return
        mcp.gpio=(mask>>16)&0x1111
        mcp2.gpio=mask&0x1111
        if check(delay):
            return
        mcp.gpio=(mask>>16)&0x9999
        mcp2.gpio=mask&0x9999
        if check(delay):
            return

def blank():
    display('        ')

starting=True    

def display(word):
    global mask,moving,starting
    set_target(word)
    mask=0xFFFFFFFF
    if starting:
        moving=[]
        starting=False
    else:
        moving=[0,1,2,3,4,5,6,7]
    while mask!=0:
        fh(0.00000,512)
    mcp.gpio=0
    mcp2.gpio=0

#display('AAAAAAAA')        
#mask=digit_mask2[3]
#while True:
#    cmd=input("Step>")
#    fh(0.00013,13)
    
#display('12345678')
#mcp.gpio=0
#mcp2.gpio=0
#GPIO.cleanup()
#sys.exit(0)
        
try:        
    #blank()
    display('NOVALABS')
    time.sleep(2)
    display(' MEETUP ')
    time.sleep(2)
    while True:
        #display('TIME IS:')
        #time.sleep(2)
        timestr=datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%I:%M%p')
        if timestr[0]=='0':
            timestr=' '+timestr[1:]
        display(timestr+' ')
        time.sleep(5)
except KeyboardInterrupt:
    blank()
    mcp.gpio=0
    mcp2.gpio=0
    GPIO.cleanup()
mcp.gpio=0
mcp2.gpio=0
GPIO.cleanup()
sys.exit(0)
