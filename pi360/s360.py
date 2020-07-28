import socket
import time
import getopt
import sys
import boto3
#from picamera import PiCamera
from os import system
import os

system("/usr/bin/killall raspistill") #in case preview is still up

s3=boto3.client('s3')
#s3r=boto3.resource('s3')

host="192.168.181.181" #adhoc address of turntable
port=8181 #port of turntable

bucket_name="<yourbucketname>"

w=None
h=None
name=None
angle=None
delay=None
dir=None
usage="Usage: python3 cam360.py -w <width> -h <height> -n <name> -a <angle> -t <delay> -d <dir>"
try:
    opts,args = getopt.getopt(sys.argv[1:],"w:h:n:a:t:d:?")
except getopt.GetoptError:
    print(usage)
    sys.exit(2)

for opt, arg in opts:
    if opt=='-?':
        print(usage)
        sys.exit()
    elif opt=='-w':
        w=int(arg)
    elif opt=='-h':
        h=int(arg)
    elif opt=='-n':
        name=arg
    elif opt=='-a':
        angle=int(arg)
    elif opt=='-t':
        delay=float(arg)
    elif opt=='-d':
        dir=int(arg)

if w==None or h==None or name==None or angle==None or delay==None or dir==None:
    print(usage)
    sys.exit(2)

def send(cmd): #send a command to the turntable
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host,port))
        s.sendall(cmd.encode())
        data = s.recv(1024)
        #print(data)

def move(dir,angle): #move cw/ccw and by angle
    send("CT+TRUNSINGLE("+str(dir)+","+str(angle)+");")

def pub_index(w,h,name): #write the index file for a subdirectory for the object
    with open('index.template.html','r') as file:
        data = file.read()
        data=data.replace("<w>",str(w))
        data=data.replace("<h>",str(h))
        data=data.replace("<name>",str(name))
        s3.put_object(Bucket=bucket_name,Key=name+'/index.html',Body=data.encode(),ContentType="text/html")
        #s3r.Object(bucket_name,name+'/index.html').put(Body=data)

def add_object(name): #append a pointer to the subdirectory for the main page
    s3.download_file(bucket_name,'objects.js','/tmp/objects.js')
    with open('/tmp/objects.js','a') as file:
        file.write('objects.push("'+name+'");\n')
    s3.upload_file('/tmp/objects.js',bucket_name,'objects.js')

#w=width
#h=height
#name=name for photo series
#delay=how many seconds between steps
#dir=0 for cw and 1 for ccw
def make360(w,h,name,angle=5,delay=0.5,dir=0):
    #cam=PiCamera()
    #cam.resolution=(w,h)
    send("CT+HEARTBEAT(0);") #turn off echo of hearbeat
    send("CT+SPKMUTE(1);") #turn off turntable beep
    steps=int(360/angle)
    pub_index(w,h,name) #add an index file for the images
    add_object(name) #add the object to the list of objects
    for i in range(steps):
        print("Angle="+str(i*angle))
        move(dir,angle) #move by 1 degree
        time.sleep(delay) #wait by delay to stabalize
        deg=i*angle
        l=i+1
        #cam.capture(name+'{0:04d}.jpg'.format(deg)) #capture to a jpeg
        filename=name+"-"+str(l)+".jpg"
        #had been using PiCamera but switched to raspistill when I needed custom shading tables then just stuck with it
        system("/usr/bin/raspistill -w "+str(w)+" -h "+str(h)+" --brightness 60 -o "+filename)
        s3.upload_file(filename,bucket_name,name+"/"+filename) #upload the file
        os.remove(filename) #remove it locally
    #print("Starting conversion...")
    #system('convert -monitor -delay 1x30 -loop 0 '+name+'*.jpg '+name+'.gif') #convert the series to a gif (only not deleted above locally)
    print("Capture complete")
    #should probably clean up individual images here if we don't want them

make360(w,h,name,angle,delay,dir)

