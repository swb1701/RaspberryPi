#First flap program when only 4-digits
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

for i in range(16):
    p=mcp.get_pin(i)
    p.switch_to_output()

def home1(channel):
    print("Detected home1")
    digit_step[0]=0

def home2(channel):
    print("Detected home2")
    digit_step[1]=0

def home3(channel):
    print("Detected home3")
    digit_step[2]=0

def home4(channel):
    print("Detected home4")
    digit_step[3]=0

digit_step=[-1,-1,-1,-1]
#digit_offset=[13,39,13,0]
digit_offset=[13+4,39+4,13,0+4]
digit_mask=[0xF0FF,0xFFF0,0xFF0F,0x0FFF] #for turning a motor off
digit_mask2=[0x0F00,0x000F,0x00F0,0xF000] #for detecting which motor is on
target=[-1,-1,-1,-1]

#set up the home interrupts
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(22,GPIO.FALLING,callback=home1,bouncetime=200)
GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(4,GPIO.FALLING,callback=home2,bouncetime=200)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(27,GPIO.FALLING,callback=home3,bouncetime=200)
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(17,GPIO.FALLING,callback=home4,bouncetime=200)

symbols=" ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:.,"

#set a target word
def set_target(word):
    word=word.ljust(4,' ')
    for i in range(4):
        loc=symbols.find(word[i])
        pos=int((loc/40)*512)
        target[i]=digit_offset[i]+pos

#check after each microstep whether a digit goal was achieved
def check(delay):
    global mask
    t0=time.time()
    #print(f"steps={digit_step}")
    for i in range(4):
        if digit_step[i]>-1 and mask&digit_mask2[i]!=0: #if we are moving the digit
            if digit_step[i]==target[i]*8: #if the target digit stop moving
                mask=digit_mask[i]&mask #mask off the digit
                print(f"steps={digit_step}")
            else:
                digit_step[i]=digit_step[i]+1 #otherwise increment
    if mask==0: #if nothing is moving then signal to exit
        return(True)
    rem=delay-(time.time()-t0) #calculate remaining delay needed (if any)
    if rem>0:
        time.sleep(delay)

def fh(delay,steps):
    for i in range(steps):
        mcp.gpio=mask&0x8888
        if check(delay):
            return
        mcp.gpio=mask&0xCCCC
        if check(delay):
            return
        mcp.gpio=mask&0x4444
        if check(delay):
            return
        mcp.gpio=mask&0x6666
        if check(delay):
            return
        mcp.gpio=mask&0x2222
        if check(delay):
            return
        mcp.gpio=mask&0x3333
        if check(delay):
            return
        mcp.gpio=mask&0x1111
        if check(delay):
            return
        mcp.gpio=mask&0x9999
        if check(delay):
            return

def blank():
    display('    ')

def display(word):
    global mask
    set_target(word)
    mask=0xFFFF
    while mask!=0:
        fh(0.00013,512)

try:
    #blank()
    while True:
        display('NOVA')
        time.sleep(2)
        display('LABS')
        time.sleep(2)
        #display('TIME')
        #time.sleep(2)
        #display(datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%I%M'))
        #time.sleep(2)
except KeyboardInterrupt:
    blank()
    mcp.gpio=0
    GPIO.cleanup()
mcp.gpio=0
GPIO.cleanup()
sys.exit(0)
