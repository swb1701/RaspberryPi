#flapgroup class controls a set of 4 digits from one MCP23017
import time
import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017
import RPi.GPIO as GPIO

class FlapGroup:

    def __init__(self,address):
        self.symbols=" ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:.,"
        self.address=address #address of MCP23017
        self.digit_step=[-1,-1,-1,-1]
        self.digit_offset=[0,0,0,0]
        self.digit_mask=[0,0,0,0]
        self.digit_mask2=[0,0,0,0]
        self.target=[-1,-1,-1,-1]
        self.chandigit=dict()
        self.i2c=busio.I2C(board.SCL,board.SDA)
        self.mcp=MCP23017(self.i2c,address=self.address)
        for i in range(16):
            p=self.mcp.get_pin(i)
            p.switch_to_output()

    def setHome(self,channel):
        d=self.chandigit[channel]
        self.digit_step[d]=0

    def setDigit(self,digit,hall,mask,offset):
        self.digit_offset[digit]=offset
        self.digit_mask2[digit]=mask
        self.digit_mask[digit]=~mask
        self.chandigit[hall]=digit
        GPIO.setup(hall,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(hall,GPIO.FALLING,callback=self.setHome,bouncetime=200)

    def redefine_callbacks(self):
        for i in self.chandigit:
            GPIO.add_event_detect(i,GPIO.FALLING,callback=self.setHome,bouncetime=200)

    def __str__(self):
        return(
        f"FlapGroup: addr={hex(self.address)}\n"+
        f"  digit_offset={self.digit_offset}\n"+
        f"  digit_mask=[{', '.join(hex(x+0x10000) for x in self.digit_mask)}]\n"+
        f"  digit_mask2=[{', '.join(hex(x) for x in self.digit_mask2)}]\n"+
        f"  chandigit={self.chandigit}")

    def set_target(self,word):
        word=word.ljust(4,' ')
        for i in range(4):
            loc=self.symbols.find(word[i])
            pos=int((loc/40)*512)
            self.target[i]=self.digit_offset[i]+pos

    def check(self,delay):
        t0=time.time()
        for i in range(4):
            if self.digit_step[i]>-1 and self.mask&self.digit_mask2[i]!=0: #if we are moving the digit
                if self.digit_step[i]==self.target[i]*8: #if the target digit stop moving
                    self.mask=self.digit_mask[i]&self.mask #mask off the digit
                    #print(f"steps={self.digit_step}")
                else:
                    self.digit_step[i]=self.digit_step[i]+1 #otherwise increment
            if self.mask==0: #if nothing is moving then signal to exit
                return(True)
        rem=delay-(time.time()-t0) #calculate remaining delay needed (if any)
        if rem>0:
            time.sleep(delay)
        
    def fh(self,delay,steps):
        for i in range(steps):
            self.mcp.gpio=self.mask&0x8888
            if self.check(delay):
                return
            self.mcp.gpio=self.mask&0xCCCC
            if self.check(delay):
                return
            self.mcp.gpio=self.mask&0x4444
            if self.check(delay):
                return
            self.mcp.gpio=self.mask&0x6666
            if self.check(delay):
                return
            self.mcp.gpio=self.mask&0x2222
            if self.check(delay):
                return
            self.mcp.gpio=self.mask&0x3333
            if self.check(delay):
                return
            self.mcp.gpio=self.mask&0x1111
            if self.check(delay):
                return
            self.mcp.gpio=self.mask&0x9999
            if self.check(delay):
                return

    def display(self,word):
        self.set_target(word)
        self.mask=0xFFFF
        while self.mask!=0:
            self.fh(0.00013,512)
        self.mcp.gpio=0


        
        

        
