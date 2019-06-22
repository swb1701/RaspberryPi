# robot.py
# Controller for AL5B Robot Arm Using PCA9685, Scott Bennett, 6/2019
from smbus import SMBus
from PCA9685 import PWM
import time
import subprocess
import math
import copy
import json
import traceback
import atexit
import board
import busio
import sys
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

fPWM = 50
i2c_address = 0x40 # (standard) adapt to your module
#channel = 0 # adapt to your wiring
a = 8.5 # adapt to your servo
b = 2 # adapt to your servo
# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)
# Create the SSD1306 OLED class.
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)
font0 = ImageFont.load_default()
font_height=14
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_height)
font2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
font_height2=12
image2 = Image.open('robot1.ppm')
image3 = Image.open('arm1.ppm')
image4 = Image.open('arm2.ppm')
cur=0
images=[image2,image3,image4]
moveDelay=0.15

# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT
button_A.pull = Pull.UP

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT
button_B.pull = Pull.UP

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT
button_L.pull = Pull.UP

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT
button_R.pull = Pull.UP

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT
button_U.pull = Pull.UP

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT
button_D.pull = Pull.UP

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT
button_C.pull = Pull.UP

#set up servo control
def setup():
 global pwm
 bus = SMBus(1) # Raspberry Pi revision 2
 pwm = PWM(bus, i2c_address)
 pwm.setFreq(fPWM)

#set angle for a servo
def setDirection(channel,direction):
 duty = a / 180 * direction + b
 pwm.setDuty(channel, duty)
 #print "direction =", direction, "-> duty =", duty

#save settings
def save():
 with open('settings.json','w') as file:
  tosave=[disk_pos,pos]
  file.write(json.dumps(tosave))

#load settings
def load():
 global pos,disk_pos
 try:
  with open('settings.json') as file:
   toread=json.load(file)
   disk_pos=toread[0]
   pos=toread[1]
 except:
  pass

#power down all servos  
def alloff():
   for i in range(16):
        pwm.setOff(i);
            
setup()

last=[-1]*16 #record last position of each servo

X=4
Y=4
Z=100 #was 90
G=90
WR=90
WA=0
tmpx=4
tmpy=4
tmpz=90
tmpg=10 #was 90
tmpwr=90 #was 90
tmpwa=-90 #was 0
A=4.75
B=5.00
rtod=57.295779

#Inverse Kinematics for the AL5B (From Lynxmotion)
def Arm(x,y,z,g,wa,wr):
 global Y,X,Z,WA,G,WR
 print("Arm x="+str(x)+",y="+str(y)+",z="+str(z)+",g="+str(g)+",wa="+str(wa)+",wr="+str(wr))
 M=math.sqrt((y*y)+(x*x))
 print("M="+str(M))
 if M<=0:
  return(1)
 A1=math.atan(y/x)
 A2=math.acos((A*A-B*B+M*M)/((A*2)*M))
 print("A1="+str(A1)+" A2="+str(A2))
 Elbow=math.acos((A*A+B*B-M*M)/((A*2)*B))
 Shoulder=A1+A2 #why isn't this A2-A1???
 Elbow=Elbow*rtod
 Shoulder=Shoulder*rtod
 if (int(Elbow)<=0 or int(Shoulder)<=0):
  return(1)
 Wris = abs(wa-Elbow-Shoulder)-90
 print("Elbow="+str(180-Elbow))
 print("Shoulder="+str(Shoulder))
 print("Wrist="+str(180-Wris))
 print("Base="+str(z))
 print("WristR="+str(wr))
 print("Gripper="+str(g))
 smove2(elbow=int(180-Elbow),shoulder=int(Shoulder),wrist=int(180-Wris),base=int(z),wristr=int(wr),gripper=int(g))
 Y=tmpy
 X=tmpx
 Z=tmpz
 WA=tmpwa
 G=tmpg
 WR=tmpwr
 return(0)

#move a combination of servos (direct moves in sequence)
def move(**args):
 for key in args.keys():
  channel=names[key]
  angle=args[key]
  setDirection(channel,angle)
  last[channel]=angle
  
def smove(**args):
 for key in args.keys():
  channel=names[key]
  angle=args[key]
  slow_move(channel,angle)
  last[channel]=angle

def smove2(**args):
 global last
 difs=[0]*16 #make a difs array for each servo
 steps=[0.0]*16 #make a steps array for each servo
 pos=[0.0]*16 #float position of each during move
 minsteps=40
 maxstep=1
 for key in args.keys():
  channel=names[key]
  angle=int(args[key])
  difs[channel]=angle-last[channel] #calculate dif for each servo
  pos[channel]=last[channel]
 maxchan=0
 maxval=abs(difs[0])
 for i in range(16):
  if abs(difs[i])>maxval: #find maximum servo move
   maxval=abs(difs[i])
   maxchan=i
 mstep=int(abs(difs[maxchan])/maxstep)
 if (mstep<1):
  mstep=1
 #mstep=abs(difs[maxchan]) #number of steps we'll use
 #if mstep<minsteps:
 # mstep=minsteps
 print("maxchan="+str(maxchan)+" dif="+str(difs[maxchan])+" mstep="+str(mstep))
 for i in range(16):
  steps[i]=1.0*difs[i]/mstep
 #print("Before:"+str(last))
 for x in range(mstep):
  #print("Step="+str(x))
  for key in args.keys():
   channel=names[key]
   pos[channel]=pos[channel]+steps[channel]
   #print("Channel "+str(channel)+" Angle="+str(pos[channel]))
   setDirection(channel,int(pos[channel]))
   last[channel]=int(pos[channel])
   #time.sleep(0.02) #determines speed of movement
 #print("After"+str(last))
  
#move a combination of servos based on an array of angles (direct moves in sequence)  
def move2(args):
 for i in range(len(args)):
  channel=i
  angle=int(args[i])
  if (angle>-1):
   slow_move(channel,angle)
   #setDirection(channel,angle)
  last[channel]=angle

def slow_move(channel,angle):
 global last
 print("slow move "+str(channel)+","+str(angle))
 if (last[channel]==-1):
  print("Direct move...")
  setDirection(channel,angle)
  last[channel]=int(angle)
 else:
  print("Stepped move...")
  angle=int(angle)
  dif=angle-int(last[channel])
  print("dif="+str(dif))
  step=int(math.copysign(1.0,dif))
  print("step="+str(step))
  for x in range(abs(dif)):
   last[channel]=last[channel]+step
   setDirection(channel,last[channel])
   time.sleep(0.01) #determines speed of movement

#0 base 0-175 (90 is center)
#1 shoulder 30-175 (30 is parallel to ground, 100 is straight up, 175 is all the way back)
#2 elbow 0-175
#3 wrist up down 10-100 (10 is straight down, 90 is parallel to ground, 110 is a bit more then hits stop)
#4 wrist rotate 0-175 (full cw vs. full ccw)
#5 gripper (10-130 open to closed) 100 can squeeze disk
#6 suction (20-175 out to in)

names={"base":0,"shoulder":1,"elbow":2,"wrist":3,"wristr":4,"gripper":5}

servo_range={"base":[0,175],"shoulder":[30,175],"elbow":[0,175],"wrist":[10,100],"wristr":[0,175],"gripper":[10,130]}

def draw_control():
 draw.rectangle((0, 0, width, height), outline=0, fill=0)
 lines=["Control Mode","Center to Exit",""]
 if not button_A.value:
  lines.append("U/D=Elbow")
  lines.append("L/R=Gripper")
 elif not button_B.value:
  lines.append("U/D=Wrist")
  lines.append("L/R=WristR")
 else:
  lines.append("U/D=Base")
  lines.append("L/R=Shoulder")
 cnt=0
 for line in lines:
  draw.text((0,cnt*font_height2),line,font=font2,fill=255)
  cnt=cnt+1
 disp.image(image)
 disp.show()

def step_servo(name,val):
 chan=names[name]
 nval=last[chan]+val
 srange=servo_range[name]
 if nval<srange[0]:
  nval=srange[0]
 elif nval>srange[1]:
  nval=srange[1]
 setDirection(chan,nval)
 last[chan]=nval

def control_loop():
 lastA=5
 lastB=5
 draw_control()
 spd=1
 while True:
  if (not button_A.value) and (not button_B.value): #hitting both buttons returns
   break
  if (not button_C.value): #hitting center returns
   break
  if (button_A.value!=lastA) or (button_B.value!=lastB):
   draw_control()
   lastA=button_A.value
   lastB=button_B.value
  if not button_U.value:
   if not button_A.value:
    #print("UA")
    step_servo("elbow",-1*spd)
   elif not button_B.value:
    #print("UB")
    step_servo("wrist",spd)
   else:
    #print("U")
    step_servo("base",-1*spd)
  elif not button_L.value:
   if not button_A.value:
    #print("LA")
    step_servo("gripper",-1*spd)
   elif not button_B.value:
    #print("LB")
    step_servo("wristr",-1*spd)
   else:
    #print("L")
    step_servo("shoulder",-1*spd)
  elif not button_D.value:
   if not button_A.value:
    #print("DA")
    step_servo("elbow",spd)
   elif not button_B.value:
    #print("DB")
    step_servo("wrist",-1*spd)
   else:
    #print("D")
    step_servo("base",spd)
  elif not button_R.value:
   if not button_A.value:
    #print("RA")
    step_servo("gripper",spd)
   elif not button_B.value:
    #print("RB")
    step_servo("wristr",spd)
   else:
    #print("R")
    step_servo("shoulder",spd)
  time.sleep(0.03)

#move(base=0,shoulder=100,elbow=100,wrist=90,wristr=90,gripper=130)
#time.sleep(5)
#move(base=90,shoulder=110,elbow=100,wrist=10,wristr=90,gripper=10)

#Arm(tmpx,tmpy,tmpz,tmpg,tmpwa,tmpwr)
#time.sleep(5)

#Elbow=109.125085498
#Shoulder=101.626045595
#Wrist=97.4990399023
#Base=90
#WristR=90
#Gripper=90

#Arm(1,tmpy,tmpz,tmpg,tmpwa,tmpwr)
#time.sleep(5)

#Elbow=130.04739484
#Shoulder=144.138221084
#Wrist=75.9091737562
#Base=90
#WristR=90
#Gripper=90

#Arm(0.001,tmpy,tmpz,tmpg,tmpwa,tmpwr)
#time.sleep(5)

#Elbow=131.641959362
#Shoulder=159.075253468
#Wrist=62.5667058938
#Base=90
#WristR=90
#Gripper=90

disk_pos=[
  [
    [4,4.4,63,-100],
    [3.9,3.5,63,-100],
    [3.65,3,63,-100],
    [3.5,2.6,63,-100],
    [3.4,2.1,63,-100],
    [3.2,1.7,64,-100],
    ],
  [
     [3.4,4,85,-100],
     [3.5,3.5,85,-100],
     [3.2,2.9,85,-100],
     [3.1,2.4,85,-100],
     [2.8,1.8,85,-100],
     [2.8,1.5,85,-100]
    ],
  [
    [4,4.4,107,-100],
    [3.8,3.65,107,-100],
    [3.6,3,107,-100],
    [3.5,2.55,107,-100],
    [3.35,2.1,107,-100],
    [3.2,1.75,107,-100]
    ]
 ]

def resetBoard():
 global board_state,board_state2
 board_state=[5,0,0]
 board_state2=[[1,2,3,4,5],[],[]]
 print("Board is Reset")

board_state=[5,0,0]
board_state2=[[1,2,3,4,5],[],[]]

step=1
def hanoi(num_disks,pfrom,pto):
 global step #declare global (to change something outside this scope)
 pusing=6-pfrom-pto #calculate temp peg from other two
 if num_disks==1: #basis of the recursion
  print("Step "+str(step)+":"+str(pfrom)+" to "+str(pto)) #print what we're moving
  move_disk(pfrom-1,pto-1)
  step=step+1 #increment our step counter
 else:
  hanoi(num_disks-1,pfrom,pusing) #move top pile to temp
  hanoi(1,pfrom,pto) #move the bottom disk to destination
  hanoi(num_disks-1,pusing,pto) #move the top pile to the destination

def move_pos(pile,pos):
 global tmpg
 val=disk_pos[pile][pos]
 if last[names['gripper']]>-1:
  tmpg=last[names['gripper']]
 Arm(float(val[0]),float(val[1]),float(val[2]),tmpg,float(val[3]),tmpwr)

def draw_tuning(pile,pos,active):
 val=disk_pos[pile][pos]
 tmpg=last[names['gripper']]
 draw.rectangle((0, 0, width, height), outline=0, fill=0)
 parms=[["X",val[0]],
        ["Y",val[1]],
        ["SA",val[2]],
        ["WA",val[3]],
        ["G",tmpg]]
 i=0
 for parm in parms:
  label=parm[0]+':'
  draw.text((0,i*font_height2),label,font=font2,fill=255)
  w,h=font2.getsize(str(parm[1]))
  if active==i:
    draw.rectangle((40,i*font_height2+1,40+w,i*font_height2+h+1),fill=255)
  if active==i:
   draw.text((40,i*font_height2),str(parm[1]),font=font2,fill=0)
  else:
   draw.text((40,i*font_height2),str(parm[1]),font=font2,fill=255)
  i=i+1
 disp.image(image)
 disp.show()
 if (active==-1):
  hitkey()
 
def tuning_loop(pile,pos):
 global disk_pos
 temp_fld=0
 draw_tuning(pile,pos,temp_fld)
 while True:
  change=0
  if not button_U.value:
   st=int(round(time.time()*1000))
   while not button_U.value and (int(round(time.time()*1000))-st)<menu_speed:
    pass
   disk_pos[pile][pos][temp_fld]=disk_pos[pile][pos][temp_fld]-0.01
   change=1
  elif not button_L.value:
   while not button_L.value:
    pass
   if (temp_fld>0):
    temp_fld=temp_fld-1
    change=1
   else:
    return(None)
  elif not button_R.value:
   while not button_R.value:
    pass
   if temp_fld<(len(disk_pos[pile][pos])):
    temp_fld=temp_fld+1
   else:
    temp_fld=0
   change=1
  elif not button_D.value:
   st=int(round(time.time()*1000))
   while not button_D.value and (int(round(time.time()*1000))-st)<menu_speed:
    pass
   disk_pos[pile][pos][temp_fld]=disk_pos[pile][pos][temp_fld]+0.01
   change=1
  elif not button_C.value:
   while not button_C.value:
    pass
   return(None)
  elif not button_A.value:
   while not button_A.value:
    pass
   move_pos(pile,pos)
  elif not button_B.value:
   while not button_B.value:
    pass
   move_pos(pile,0)
  if change==1:
   draw_tuning(pile,pos,temp_fld)

def move_disk(pfrom,pto):
 global board_state
 print(board_state)
 d=moveDelay
 print("Move Disk From "+str(pfrom)+" to "+str(pto)+" dly="+str(d))
 o=65
 smove2(gripper=o) #open gripper
 move_pos(pfrom,0) #above from pile
 time.sleep(d)
 move_pos(pfrom,5-board_state[pfrom]+1)
 time.sleep(d)
 smove2(gripper=110) #close gripper
 time.sleep(d)
 move_pos(pfrom,0) #above from pile
 time.sleep(d)
 move_pos(pto,0) #above to pile
 time.sleep(d)
 move_pos(pto,5-board_state[pto])
 time.sleep(d)
 smove2(gripper=o) #open gripper
 time.sleep(d)
 move_pos(pto,0) #above to pile
 board_state[pfrom]=board_state[pfrom]-1
 board_state[pto]=board_state[pto]+1
 dsk=board_state2[pfrom].pop(0)
 board_state2[pto].insert(0,dsk)
 print(board_state)
 print(board_state2)
 draw_disks()

def fling_disk(pfrom):
 global board_state
 print(board_state)
 d=moveDelay
 print("Fling Disk From "+str(pfrom)+" dly="+str(d))
 o=65
 smove2(gripper=o) #open gripper
 move_pos(pfrom,0) #above from pile
 time.sleep(d)
 move_pos(pfrom,5-board_state[pfrom]+1)
 time.sleep(d)
 smove2(gripper=110) #close gripper
 time.sleep(d)
 move_pos(pfrom,0) #above from pile
 time.sleep(d)
 smove2(wrist=90)
 move(base=170)
 #move(base=0,gripper=10)
 move(base=0)
 move(gripper=10)
 board_state[pfrom]=board_state[pfrom]-1
 dsk=board_state2[pfrom].pop(0)
 draw_disks()

def tantrum():
 for i in range(5):
  fling_disk(0)
 alloff()
 resetBoard()

@atexit.register
def shutdown():
 move2(pos["home"]) #move to home preset
 time.sleep(0.5)
 alloff()
 save()
 disp.fill(0)
 disp.show()
 print("Goodbye!")

def draw_screen():
        draw.polygon([(20, 20), (30, 2), (40, 20)], outline=255, fill=0)  #Up
        draw.polygon([(0, 30), (18, 21), (18, 41)], outline=255, fill=0)  #left
        draw.polygon([(60, 30), (42, 21), (42, 41)], outline=255, fill=0) #right
        draw.polygon([(30, 60), (40, 42), (20, 42)], outline=255, fill=0) #down
        draw.rectangle((20, 22, 40, 40), outline=255, fill=0) #center
        draw.ellipse((70, 40, 90, 60), outline=255, fill=0) #A button
        draw.ellipse((100, 20, 120, 40), outline=255, fill=0) #B button
        disp.image(image)
        disp.show()

def draw_disks():
 disp.fill(0)
 draw.rectangle((0, 0, width, height), outline=0, fill=0)
 disk_height=5
 disk_width=30
 disk_gap=3
 peg_height=6*(disk_height+disk_gap)
 peg_width=3
 peg_gap=(width-3*peg_width)/4
 for i in range(3):
  left=peg_gap*(i+1)+peg_width*i
  draw.rectangle((left,height-peg_height,left+peg_width,height),outline=255,fill=1)
  j=0
  for dsk in board_state2[i][::-1]:
   draw.rectangle((left-(disk_width-5*((6-dsk)-1))/2+1,height-(j+1)*disk_gap-j*disk_height,left+(disk_width-5*((6-dsk)-1))/2+1,height-(j+1)*disk_gap-(j+1)*disk_height),outline=255,fill=1)
   j=j+1
 disp.image(image)
 disp.show()

pos={}

load()
move2(pos["home"]) #move to home preset
time.sleep(0.5)
alloff()

interactive=0

if interactive==1:
 # Clear display.
 disp.fill(0)
 disp.show()
 draw_disks()
 #Main Interactive Control Loop
 while True:
  try:
   cmd=input("Servo,Angle->")
   if (cmd[0]=="q"): #quit
    break
   if (cmd[0]=="b"): #reset board
    board_state=[5,0,0]
    board_state2=[[1,2,3,4,5],[],[]]
    continue
   if (cmd[0]=="o"): #motors off
    alloff()
    continue
   if (cmd[0]=="d"): #disk move
    parts=cmd[1:].split(",")
    move_disk(int(parts[0])-1,int(parts[1])-1)
    continue
   if (cmd[0]=="h"): #hanoi move (disk, frompile, topile)
    step=1
    parts=cmd[1:].split(",")
    hanoi(int(parts[0]),int(parts[1]),int(parts[2]))
    continue
   if (cmd[0]=="p"): #pos move (piles 1,2, and 3)
    parts=cmd[1:].split(",")
    move_pos(int(parts[0])-1,int(parts[1]))
    continue
   if (cmd[0]=="x"): #inverse kinematics x,y move in format x<x>,<y>
    parts=cmd[1:].split(',')
    if last[names['gripper']]>-1:
     tmpg=last[names['gripper']]
     #if last[names['wrist']]>-1:
     # tmpwa=last[names['wrist']]
     #if last[names['wristr']]>-1:
     # tmpwr=last[names['wristr']]
     Arm(float(parts[0]),float(parts[1]),float(parts[2]),tmpg,float(parts[3]),tmpwr)
     continue
    if (cmd[0]=="s"): #save preset in form s<name>
     key=cmd[1:]
     pos[key]=copy.deepcopy(last)
     save()
     continue
    if (cmd[0]=="r"): #restore preset in form r<name>
     load()
     key=cmd[1:]
     move2(pos[key])
     continue
    if (cmd[0]=="f"): #restore preset in form r<name>
     load()
     key=cmd[1:]
     last=[-1]*16 #record last position of each servo
     move2(pos[key])
     continue
    if (cmd[0]=="m"): #servo move in form <name>,<angle>
     parts=cmd[1:].split(",")
     channel=names[parts[0]]
     angle=int(parts[1])
     slow_move(channel,angle)
     continue
    parts=cmd.split(',') #move individual servo in form <channel>,<angle>
    channel=int(parts[0])
    angle=int(parts[1])
    slow_move(channel,angle)
  except Exception:
   traceback.print_exc()
   continue

def hitkey():  
 while True:
  if not button_L.value:
   while not button_L.value:
    pass
   break
  if not button_R.value:
   while not button_R.value:
    pass
   break
  if not button_U.value:
   while not button_U.value:
    pass
   break
  if not button_D.value:
   while not button_D.value:
    pass
   break
  if not button_C.value:
   while not button_C.value:
    pass
   break
  
def holdingkey():
  if not button_L.value:
   return(True)
  if not button_R.value:
   return(True)
  if not button_U.value:
   return(True)
  if not button_D.value:
   return(True)
  if not button_C.value:
   return(True)
  return(False)

def showInfo():
 draw.rectangle((0, 0, width, height), outline=0, fill=0)
 cmd = "hostname -I | cut -d\' \' -f1"
 IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
 cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
 CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
 cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
 MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
 cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%d GB  %s\", $3,$2,$5}'"
 Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
 draw.text((0, 0), "IP: "+IP, font=font0, fill=255)
 draw.text((0, 10), CPU, font=font0, fill=255)
 draw.text((0, 20), MemUsage, font=font0, fill=255)
 draw.text((0, 30), Disk, font=font0, fill=255)
 disp.image(image)
 disp.show()
 hitkey()

def moveDisk():
 print("TBD")

def runHanoi(disks,fpeg,tpeg):
 global steps
 print("disks="+str(disks)+",fpeg="+str(fpeg)+",tpeg="+str(tpeg))
 steps=1
 hanoi(disks,fpeg,tpeg)

def setSpeed(spd):
 global moveDelay
 print("Setting move delay to "+str(spd))
 moveDelay=spd

def moveLeft(pos):
 move_pos(0,pos)

def moveCenter(pos):
 move_pos(1,pos)

def moveRight(pos):
 move_pos(2,pos)

def relax():
 alloff()

def get_field(idx,args): 
 arg=args[idx]
 usefield=0
 cnt=0
 for fld in arg:
  if 'default' in fld:
   usefield=cnt
  cnt=cnt+1
 return(usefield)

def draw_template(temp,temp_fld,temp_vals):
 draw.rectangle((0, 0, width, height), outline=0, fill=0)
 text=temp['text']
 args=temp['args']
 ah=4
 fld_cnt=-1
 for i in range(len(text)):
  line=text[i]
  pos=0
  parts=[]
  fld_start=fld_cnt
  while True:
   hit=line.find('$',pos)
   if hit==-1:
    parts.append([0,line[pos:]])
    break
   else:
    parts.append([0,line[pos:hit]])
    num=int(line[hit+1:hit+2])
    pos=hit+2
    #parts.append([1,get_field_value(num,args)])
    fld_cnt=fld_cnt+1
    parts.append([1,args[num][temp_vals[fld_cnt]]['name']])
  #print(parts)
  pos=5
  fld_cnt=fld_start
  for part in parts:
   if part[0]==1:
    fld_cnt=fld_cnt+1
   w,h=font.getsize(part[1])
   if part[0]==1 and temp_fld==fld_cnt:
    draw.rectangle((pos,i*(font_height+ah)+1,pos+w,i*(font_height+ah)+h),fill=255)
   if part[0]==1 and temp_fld==fld_cnt:
    draw.text((pos,i*(font_height+ah)),part[1],font=font,fill=0)
   else:
    draw.text((pos,i*(font_height+ah)),part[1],font=font,fill=255)
   pos=pos+w
 disp.image(image)
 disp.show()
 #hitkey()

def template_loop(temp):
 temp_fld=0
 if 'vals' in temp:
  temp_vals=temp['vals']
 else:
  temp_vals=[]
  for i in range(len(temp['args'])):
   temp_vals.append(get_field(i,temp['args']))
 draw_template(temp,temp_fld,temp_vals)
 while True:
  change=0
  if not button_U.value:
   st=int(round(time.time()*1000))
   while not button_U.value and (int(round(time.time()*1000))-st)<menu_speed:
    pass
   if temp_vals[temp_fld]>0:
    temp_vals[temp_fld]=temp_vals[temp_fld]-1
    temp['vals']=temp_vals
    change=1
  elif not button_L.value:
   while not button_L.value:
    pass
   return(None)
  elif not button_R.value:
   while not button_R.value:
    pass
   if temp_fld<(len(temp['args'])-1):
    temp_fld=temp_fld+1
    change=1
  elif not button_D.value:
   st=int(round(time.time()*1000))
   while not button_D.value and (int(round(time.time()*1000))-st)<menu_speed:
    pass
   if temp_vals[temp_fld]<(len(temp['args'][temp_fld])-1):
    temp_vals[temp_fld]=temp_vals[temp_fld]+1
    temp['vals']=temp_vals
    change=1
  elif not button_C.value:
   while not button_C.value:
    pass
   result=[]
   cnt=0
   for val in temp_vals:
    result.append(temp['args'][cnt][val]['value'])
    cnt=cnt+1
   return(result)
  if change==1:
   draw_template(temp,temp_fld,temp_vals)

disk_move_template={
 "text": [
  "Move Disks",
  "From $0 Peg",
  "To $1 Peg"
  ],
 "args": [
  [{"name":"Left","value":0,"default":1},{"name":"Center","value":1},{"name":"Right","value":2}],
  [{"name":"Left","value":0},{"name":"Center","value":1},{"name":"Right","value":2,"default":1}]
  ]
}

hanoi_template={
 "text": [
  "Move $0 Disk(s)",
  "From $1 Peg",
  "To $2 Peg"
  ],
 "args": [
  [{"name":"1","value":1},{"name":"2","value":2},{"name":"3","value":3},{"name":"4","value":4},{"name":"5","value":5}],
  [{"name":"Left","value":1,"default":1},{"name":"Center","value":2},{"name":"Right","value":3}],
  [{"name":"Left","value":1},{"name":"Center","value":2},{"name":"Right","value":3,"default":1}]
  ]
}

speed_template={
 "text": [
  "Delay $0 Ms",
  "Between Moves"
  ],
 "args": [
  ]
}

lst=speed_template['args']
lst2=[]
vl0=0.15
for i in range(21):
 vl=(0.01*i)
 if (vl==0.15):
  lst2.append({"name":str(vl),"value":vl,"default":1})
 else:
  lst2.append({"name":str(vl),"value":vl})
lst.append(lst2)  

def test_temp():
 result=template_loop(disk_move_template)
 print("result="+str(result))

def gen_arm_menu(name,action,pile):
 sub=[]
 for i in range(6):
  subsub=[
     {"name":"View","action":draw_tuning,"args":{"pile":pile,"pos":i,"active":-1}},
     {"name":"Edit","action":tuning_loop,"args":{"pile":pile,"pos":i}}
  ]
  sub.append({"name":"Level "+str(i),"action":action,"args":{"pos":i},"submenu":subsub})
 map={"name":name,"action":action,"args":{"pos":0},"submenu":sub}
 return(map)

menu=[
 {"name":"Info","action":showInfo},
 {"name":"Hanoi","submenu":[
  {"name":"Move Arm","submenu":[
   gen_arm_menu("Left Peg",moveLeft,0),
   gen_arm_menu("Center Peg",moveCenter,1),
   gen_arm_menu("Right Peg",moveRight,2),
   {"name":"Motors Off","action":relax}
   ]},
  {"name":"Move Disk","action":move_disk,"template":disk_move_template},
  {"name":"Run Hanoi","action":runHanoi,"template":hanoi_template},
  {"name":"Misc Routines","submenu":[
   {"name":"Fling","action":fling_disk,"args":{"pfrom":0}},
   {"name":"Tantrum","action":tantrum}
  ]}
 ]},
 {"name":"Manual Ctrl","action":control_loop},
 {"name":"Settings","submenu":[
  {"name":"Speed","action":setSpeed,"template":speed_template},
  {"name":"Reset Board","action":resetBoard}
  ]}
]

menu_stack=[]
menu_cur=menu
menu_top=0
menu_pos=0
menu_height=4
menu_speed=150

def draw_menu():
 draw.rectangle((0, 0, width, height), outline=0, fill=0)
 bot=menu_top+menu_height-1
 if bot>(len(menu_cur)-1):
  bot=len(menu_cur)-1
 srow=0
 sleft=14
 for row in range(bot-menu_top+1):
  idx=row+menu_top
  draw.text((sleft,row*font_height),menu_cur[idx]['name'],font=font,fill=255)
  if idx==menu_pos:
   draw.text((0,row*font_height-2),">",font=font,fill=255)
  if 'submenu' in menu_cur[idx]:
   draw.text((width-14,row*font_height),">",font=font,fill=255)
 disp.image(image)
 disp.show()

def menu_loop():
 global menu_stack,menu_cur,menu_pos,menu_top,cur
 draw_menu()
 st=int(round(time.time()*1000))
 while True:
  if (int(round(time.time()*1000))-st)>120000: #sleep after 2 mins
   alloff()
   while True:
    for i in range(80):
     draw.rectangle((0, 0, width, height), outline=0, fill=0)
     image.paste(images[cur],((i-20)*3,0))
     disp.image(image)
     disp.show()
     if holdingkey():
      break
    cur=(cur+1)%3
    if holdingkey():
     break
   hitkey()
   st=int(round(time.time()*1000))
   draw_menu()
  change=0
  if not button_U.value:
   st=int(round(time.time()*1000))
   while not button_U.value and (int(round(time.time()*1000))-st)<menu_speed:
    pass
   menu_pos=menu_pos-1
   if menu_pos<0:
    menu_pos=0
   if menu_pos<menu_top:
    menu_top=menu_pos
   change=1
  elif not button_L.value:
   while not button_L.value:
    pass
   if len(menu_stack)>0:
    oldm=menu_stack.pop(0)
    menu_cur=oldm[0]
    menu_pos=oldm[1]
    menu_top=oldm[2]
    change=1
  elif not button_R.value:
   while not button_R.value:
    pass
   if 'submenu' in menu_cur[menu_pos]:
    menu_stack.insert(0,[menu_cur,menu_pos,menu_top])
    menu_cur=menu_cur[menu_pos]['submenu']
    menu_pos=0
    menu_top=0
    change=1
   elif 'action' in menu_cur[menu_pos]:
    if 'args' in menu_cur[menu_pos]:
     args=menu_cur[menu_pos]['args']
     menu_cur[menu_pos]['action'](**args)
    else:
     if 'template' in menu_cur[menu_pos]:
      args=template_loop(menu_cur[menu_pos]['template'])
      if args!=None:
       try:
        menu_cur[menu_pos]['action'](*args)
       except:
        pass
     else:
      try:
       menu_cur[menu_pos]['action']()
      except:
       pass
    change=1
  elif not button_D.value:
   st=int(round(time.time()*1000))
   while not button_D.value and (int(round(time.time()*1000))-st)<menu_speed:
    pass
   menu_pos=menu_pos+1
   if menu_pos>(len(menu_cur)-1):
    menu_pos=len(menu_cur)-1
   if menu_pos>(menu_top+menu_height-1):
    menu_top=menu_top+1
   change=1
  elif not button_C.value:
   while not button_C.value:
    pass
   if 'action' in menu_cur[menu_pos]:
    if 'args' in menu_cur[menu_pos]:
     args=menu_cur[menu_pos]['args']
     try:
      menu_cur[menu_pos]['action'](**args)
     except:
      pass
    else:
     if 'template' in menu_cur[menu_pos]:
      args=template_loop(menu_cur[menu_pos]['template'])
      if args!=None:
       try:
        menu_cur[menu_pos]['action'](*args)
       except:
        pass
     else:
      try:
       menu_cur[menu_pos]['action']()
      except:
       pass
    change=1
   elif 'submenu' in menu_cur[menu_pos]:
    menu_stack.insert(0,[menu_cur,menu_pos,menu_top])
    menu_cur=menu_cur[menu_pos]['submenu']
    menu_pos=0
    change=1
  if change==1:
   draw_menu()
   st=int(round(time.time()*1000))

menu_loop()


