# Cylinder Gadget (based on Amazon example code & Scott's original cylinder light)

import logging
import sys
import time
import board
import neopixel
import random
import threading
import dateutil.parser
import traceback
import json
import color_constants

from agt import AlexaGadget

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 484
rows=10
cols=44

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)

colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255),(255,255,255),(255,0,0),(0,255,0),(0,0,255),(255,255,0)]

font_data = [0x00, 0x00, 0x00, 0x00, 0x00, # ''
0x00, 0x00, 0x17, 0x00, 0x00, # '!'
0x00, 0x03, 0x00, 0x03, 0x00, # '"'
0x0a, 0x1f, 0x0a, 0x1f, 0x0a, # '#'
0x12, 0x15, 0x1f, 0x15, 0x09, # '$'
0x13, 0x0b, 0x04, 0x1a, 0x19, # '%'
0x0d, 0x12, 0x15, 0x08, 0x14, # '&'
0x00, 0x00, 0x03, 0x00, 0x00, # '''
0x00, 0x0e, 0x11, 0x00, 0x00, # '('
0x00, 0x00, 0x11, 0x0e, 0x00, # ')'
0x00, 0x05, 0x02, 0x05, 0x00, # '*'
0x04, 0x04, 0x1f, 0x04, 0x04, # '+'
0x00, 0x10, 0x08, 0x00, 0x00, # ','
0x04, 0x04, 0x04, 0x04, 0x04, # '-'
0x00, 0x18, 0x18, 0x00, 0x00, # '.'
0x10, 0x08, 0x04, 0x02, 0x01, # '/'
0x0e, 0x11, 0x15, 0x11, 0x0e, # '0'
0x00, 0x12, 0x1f, 0x10, 0x00, # '1'
0x00, 0x1d, 0x15, 0x15, 0x17, # '2'
0x00, 0x11, 0x15, 0x15, 0x0e, # '3'
0x00, 0x07, 0x04, 0x04, 0x1f, # '4'
0x00, 0x17, 0x15, 0x15, 0x09, # '5'
0x00, 0x1f, 0x15, 0x15, 0x1d, # '6'
0x00, 0x03, 0x19, 0x05, 0x03, # '7'
0x00, 0x0a, 0x15, 0x15, 0x0a, # '8'
0x00, 0x02, 0x15, 0x15, 0x0e, # '9'
0x00, 0x00, 0x12, 0x00, 0x00, # ':'
0x00, 0x08, 0x1a, 0x00, 0x00, # ';'
0x00, 0x04, 0x0a, 0x11, 0x00, # '<'
0x00, 0x0a, 0x0a, 0x0a, 0x0a, # '='
0x00, 0x11, 0x0a, 0x04, 0x00, # '>'
0x00, 0x01, 0x15, 0x05, 0x02, # '?'
0x0e, 0x11, 0x15, 0x05, 0x06, # '@'
0x00, 0x1f, 0x05, 0x05, 0x1f, # 'A'
0x00, 0x1f, 0x15, 0x15, 0x0e, # 'B'
0x00, 0x0e, 0x11, 0x11, 0x0a, # 'C'
0x00, 0x1f, 0x11, 0x11, 0x0e, # 'D'
0x00, 0x1f, 0x15, 0x15, 0x11, # 'E'
0x00, 0x1f, 0x05, 0x05, 0x01, # 'F'
0x00, 0x0e, 0x11, 0x15, 0x1d, # 'G'
0x00, 0x1f, 0x04, 0x04, 0x1f, # 'H'
0x00, 0x11, 0x1f, 0x11, 0x00, # 'I'
0x00, 0x18, 0x10, 0x10, 0x1f, # 'J'
0x00, 0x1f, 0x04, 0x0a, 0x11, # 'K'
0x00, 0x1f, 0x10, 0x10, 0x10, # 'L'
0x1f, 0x02, 0x0c, 0x02, 0x1f, # 'M'
0x00, 0x1f, 0x06, 0x0c, 0x1f, # 'N'
0x00, 0x0e, 0x11, 0x11, 0x0e, # 'O'
0x00, 0x1f, 0x05, 0x05, 0x02, # 'P'
0x00, 0x0e, 0x15, 0x19, 0x1e, # 'Q'
0x00, 0x1f, 0x05, 0x0d, 0x12, # 'R'
0x00, 0x12, 0x15, 0x15, 0x09, # 'S'
0x01, 0x01, 0x1f, 0x01, 0x01, # 'T'
0x00, 0x0f, 0x10, 0x10, 0x0f, # 'U'
0x03, 0x0c, 0x10, 0x0c, 0x03, # 'V'
0x0f, 0x10, 0x0c, 0x10, 0x0f, # 'W'
0x11, 0x0a, 0x04, 0x0a, 0x11, # 'X'
0x01, 0x02, 0x1c, 0x02, 0x01, # 'Y'
0x00, 0x19, 0x15, 0x13, 0x11, # 'Z'
0x00, 0x1f, 0x11, 0x11, 0x00, # '['
0x01, 0x02, 0x04, 0x08, 0x10, # '\'
0x00, 0x11, 0x11, 0x1f, 0x00, # ']'
0x00, 0x02, 0x01, 0x02, 0x00, # '^'
0x10, 0x10, 0x10, 0x10, 0x10, # '_'
0x00, 0x01, 0x02, 0x00, 0x00, # '`'
0x00, 0x08, 0x1a, 0x1a, 0x1c, # 'a'
0x00, 0x1f, 0x14, 0x14, 0x08, # 'b'
0x00, 0x0c, 0x12, 0x12, 0x12, # 'c'
0x00, 0x08, 0x14, 0x14, 0x1f, # 'd'
0x00, 0x0c, 0x16, 0x16, 0x14, # 'e'
0x00, 0x04, 0x1e, 0x05, 0x01, # 'f'
0x00, 0x0c, 0x12, 0x1a, 0x08, # 'g'
0x00, 0x1f, 0x04, 0x04, 0x18, # 'h'
0x00, 0x14, 0x14, 0x1d, 0x10, # 'i'
0x00, 0x18, 0x10, 0x10, 0x1d, # 'j'
0x00, 0x1f, 0x08, 0x0c, 0x10, # 'k'
0x00, 0x11, 0x1f, 0x10, 0x00, # 'l'
0x1e, 0x02, 0x1e, 0x02, 0x1c, # 'm'
0x00, 0x1e, 0x02, 0x02, 0x1c, # 'n'
0x00, 0x0c, 0x12, 0x12, 0x0c, # 'o'
0x00, 0x1e, 0x0a, 0x0a, 0x04, # 'p'
0x00, 0x04, 0x0a, 0x0a, 0x1e, # 'q'
0x00, 0x1c, 0x02, 0x02, 0x02, # 'r'
0x00, 0x14, 0x1e, 0x1a, 0x0a, # 's'
0x00, 0x04, 0x0f, 0x14, 0x10, # 't'
0x00, 0x0e, 0x10, 0x10, 0x1e, # 'u'
0x00, 0x06, 0x18, 0x18, 0x06, # 'v'
0x0e, 0x10, 0x0e, 0x10, 0x0e, # 'w'
0x00, 0x12, 0x0c, 0x0c, 0x12, # 'x'
0x00, 0x02, 0x14, 0x1c, 0x02, # 'y'
0x00, 0x12, 0x1a, 0x16, 0x12, # 'z'
0x00, 0x04, 0x1f, 0x11, 0x11, # '{'
0x00, 0x00, 0x1f, 0x00, 0x00, # '|'
0x00, 0x11, 0x11, 0x1f, 0x04, # '}'
0x00, 0x01, 0x03, 0x02, 0x02] # '~'

class CylinderGadget(AlexaGadget):

    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.main_thread = threading.Thread(target=self.main_loop)
        self.main_thread.start()
        self.wake=False
        self.indicate=False
        self.timer_end_time=None
        self.timer_token=None
        self.timer_active=False
        self.timer_ringing=False
        self.scroll_text=None
        self.scroll_time=False
        self.fcolor=(0,255,0)
        self.fcolor0=(0,255,0)
        self.bcolor=(0,0,0)
        self.bcolor0=(0,0,0)

    def get_color(self,name):
        c=color_constants.colors[name]
        return(c[0],c[1],c[2])
        
    def on_custom_cylinderlightgadget_message(self, directive):
        payload = json.loads(directive.payload.decode("utf-8"))
        print(payload)
        if 'message' in payload:
            if payload['message'].upper()=='TIME':
                self.scroll_time=True
                self.start_scroll(self.get_time(),self.fcolor,10)
            else:
                self.start_scroll(payload['message'].upper(),self.fcolor,10)
        if 'clear' in payload:
            try:
                self.scroll_text=None
                self.scroll_time=False
            except:
                pass
        if 'next' in payload:
            try:
                print("next TBD")
            except:
                pass
        if 'fcolor' in payload:
            try:
                self.fcolor=self.get_color(payload['fcolor'])
                print("fcolor="+self.fcolor)
            except:
                pass
        if 'bcolor' in payload:
            try:
                self.bcolor=self.get_color(payload['bcolor'])
                print("bcolor="+self.bcolor)
            except:
                pass

    def on_connected(self, device_addr):
        print("Connected")

    def on_disconnected(self, device_addr):
        self.timer_ringing=False
        print("Disconnected")

    def on_alexa_gadget_statelistener_stateupdate(self, directive):
        for state in directive.payload.states:
            if state.name == 'wakeword':
                if state.value == 'active':
                    self.wake=True
                elif state.value == 'cleared':
                    self.wake=False

    def on_notifications_setindicator(self, directive):
        self.indicate=True
        print("Set Notification Indicator")

    def on_notifications_clearindicator(self, directive):
        self.indicate=False
        print("Clear Notification Indicator")

    def on_alexa_gadget_speechdata_speechmarks(self, directive):
        #print("Got speechmarks")
        pass

    def on_alexa_gadget_musicdata_tempo(self, directive):
        print("Got tempo")

    def on_alerts_setalert(self, directive):
        if directive.payload.type != 'TIMER':
            print("Skipping non timer alerts")
            return
        t = dateutil.parser.parse(directive.payload.scheduledTime).timestamp()
        print("t="+str(t))
        if t<=0:
            return
        if self.timer_token==directive.payload.token:
            self.timer_end_time=t #adjustment to end time
            print("Adjust timer to "+str(t))
            return
        if self.timer_active:
            print("Timer already active -- only supporting one for now")
            return
        self.timer_end_time = t
        self.timer_token = directive.payload.token
        self.timer_active = True
        print("Starting timer for "+str(t))

    def on_alerts_deletealert(self, directive):
        if self.timer_token != directive.payload.token:
            print("Skipping delete alert for non-active timer")
            return
        print("Turning off timer")
        self.timer_active=False
        self.timer_token=None

    def render_char(self, s,c,col):
        offset=(ord(c)-32)*5
        w=0
        k=0
        c2=0
        for i in range(5):
            c2=font_data[offset+i]
            if (c2!=0 or c==' '):
                w=w+1
                mask=0x10
                for j in range(5):
                    if (c2&mask)!=0:
                        if ((s+i)>=0 and (s+i)<44):
                            pixels[self.pix(4-j+3,s+k)]=col
                    mask=mask>>1
                k=k+1
        return(w)

    def render_string(self,start,string,color):
        i=0
        while(start<44 and i<len(string)):
            w=self.render_char(start,string[i],color)
            start=start+w+1
            i=i+1

    def scroll_string(self,string,color,num):
        for i in range(num):
            p=43
            while(p>(-6*len(string))):
                for i in range(num_pixels):
                    pixels[i]=self.bcolor
                self.render_string(p,string,color)
                pixels.show()
                #time.sleep(0.01)
                p=p-1

    def start_scroll(self,string,color,num):
        self.p=43
        self.scroll_text=string
        self.scroll_color=color
        self.scroll_count=num

    def scroll_step(self):
        if(self.p>(-6*len(self.scroll_text))):
            #for i in range(num_pixels):
            #    pixels[i]=self.bcolor
            self.render_string(self.p,self.scroll_text,self.scroll_color)
            #pixels.show()
            self.p=self.p-1
        else:
            self.p=43 #change to scroll forever until cleared
            if self.scroll_time:
                self.scroll_text=self.get_time()

    def get_time(self):
        t=time.strftime("%I:%M")
        if t[0]=='0':
            t=t[1:]
        return(t)

    def show_time(self,color):
        t=time.strftime("%I:%M")
        if t[0]=='0':
            t=t[1:]
        self.scroll_string(t,(255,0,0),3)

    def wheel(self,pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)
        return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


    def rainbow_cycle(self,wait):
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            #time.sleep(wait)
            
    def pixel_test(self):        
        for i in range(num_pixels):
            pixels[i]=(255,0,0)
            pixels.show()
            #time.sleep(0.1)

    def blank(self):        
        for i in range(num_pixels):
            pixels[i]=self.bcolor
        pixels.show()

    def vertical_sweep(self):
        for i in range(500):
            s=i%20
            for i in range(num_pixels):
                pixels[i]=self.bcolor
            for i in range(5):
                pixels[s*5+i]=(0,255,0)
            pixels.show()
            time.sleep(0.01)

    def ring(self,color):
        for c in range(cols):
            pixels[self.pix(0,c)]=color

    def multi_color(self):
        temp=[0,0,0,0,0,0,0,0,0,0,0]
        for i in range(num_pixels):
            pixels[i]=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        for j in range(num_pixels*5):
            for i in range(11):
                temp[i]=pixels[self.pix(i,0)]
            for i in range(11):
                for k in range(43):
                    pixels[self.pix(i,k)]=pixels[self.pix(i,k+1)]
        for i in range(11):
            pixels[self.pix(i,43)]=temp[i]
        pixels.show()
        time.sleep(0.05)
        
    def multi_color2(self):
        self.blank()
        for i in range(500):
            for i in range(5):
                pixels[i]=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            for i in range(19):
                for j in range(5):
                    pixels[5+(18-i)*5+j]=pixels[5+((18-i)-1)*5+j]
            pixels.show()
            time.sleep(0.5)

    def pix(self,row,col):
        return(row*44+(row%2)*(43-col)+(1-row%2)*col)

    def spin(self,delay,steps):
        temp=[0,0,0,0,0,0,0,0,0,0,0]
        for j in range(steps):
            for i in range(11):
                temp[i]=pixels[self.pix(i,0)]
            for i in range(11):
                for k in range(43):
                    pixels[self.pix(i,k)]=pixels[self.pix(i,k+1)]
            for i in range(11):
                pixels[self.pix(i,43)]=temp[i]
            pixels.show()
            #time.sleep(delay)

    def stripes(self,step,r,w):
        for row in range(rows):
            for col in range(cols):
                if ((col+row)%step==0):
                    pixels[self.pix(row,col)]=r#colors[(col+row)%11]
                else:
                    pixels[self.pix(row,col)]=w
        pixels.show()

    def rect(self):
        self.blank()
        for i in range(20):
            pixels[self.pix(0,i)]=(255,0,0)
            pixels[self.pix(4,i)]=(255,0,0)
        for i in range(5):
            pixels[self.pix(i,0)]=(0,255,0)
            pixels[self.pix(i,19)]=(0,0,255)
        pixels.show()
        time.sleep(30)

    def zigzag(self):
        f=True
        c=(255,0,0)
        for i in range(500):
            if (i%20)==0:
                c=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            if (i%5)==0:
                f=not f
            row=i%5
            if f:
                row=4-row
            pixels[self.pix(row,i%20)]=c
            pixels.show()
            time.sleep(0.1)

    def countdown(self,height):
        #print("height="+str(height))
        for c in range(cols):
            for r in range(10-height):
                pixels[self.pix(r+1,c)]=self.bcolor #paint black at the top
            for r in range(height):
                pixels[self.pix(10-r,c)]=(255,0,0) #and red at the bottom

    def main_loop(self):
        self.fcolor=(0,255,0)
        self.fcolor0=(0,255,0)
        self.bcolor=(0,0,0)
        self.bcolor0=(0,0,0)
        self.blank()
        cnt=0
        lit=True
        while True:
            cnt=cnt+1
            try:
                if self.bcolor!=self.bcolor0: #if background color changed
                    for i in range(num_pixels):
                        if (i>=44):
                            pixels[i]=self.bcolor #color all background
                        else:
                            pixels[i]=(0,0,0)
                    self.bcolor0=self.bcolor
                if self.fcolor!=self.fcolor0: #if foreground color changed
                    self.scroll_color=self.fcolor #set it for scrolling
                    self.fcolor0=self.fcolor
                for i in range(num_pixels): #fill the background
                    if (i>=44):
                        pixels[i]=self.bcolor #color all background
                    else:
                        pixels[i]=(0,0,0)
                if self.timer_ringing and not self.timer_active:
                    self.countdown(0)
                    self.timer_ringing=False
                if self.timer_active:
                    rem=self.timer_end_time-time.time() #calculate second remaining
                    self.time_remaining=int(rem)
                    #print("time remaining = "+str(self.time_remaining))
                    if rem<=0 and not self.timer_ringing: #if our timer went off set it inactive
                        print("Timer ringing")
                        self.timer_ringing=True
                    if self.timer_ringing:
                        if lit:
                            self.countdown(10)
                        else:
                            self.countdown(0)
                        if cnt%10==0:
                            lit=not lit
                    elif self.time_remaining<11: #check if we're in the final 10 seconds
                        self.countdown(self.time_remaining) #illustrate the countdown
                    else:
                        pass #consider displaying time remaining in seconds in digits or something
                if (self.scroll_text!=None): #draw any scrolling text
                    self.scroll_step()
                if (self.wake):
                    self.ring((0,0,255)) #blue for wakeword
                else:
                    if (self.indicate):
                        self.ring((255,255,0)) #yellow for notification
                pixels.show()
            except:
                traceback.print_exc()
            #self.blank()
            #self.stripes(4,(255,0,0),(0,0,0))
            #self.spin(0.0,40)
            #self.stripes(4,(0,0,255),(0,0,0))
            #self.spin(0.0,40)
            #self.stripes(4,(0,255,0),(0,0,0))
            #self.spin(0.0,40)
            #self.show_time((255,0,0))
            #self.scroll_string("DO YOU LIKE THE CYLINDER LIGHT?",(0,255,0),1)

if __name__ == '__main__':
    CylinderGadget().main()
