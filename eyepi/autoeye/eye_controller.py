import io
import time
import picamera
#from base_camera import BaseCamera
import cv2
import numpy
import imutils
import pickle
import socket
from threading import Thread, Lock, Condition

class EyeController(Thread):

    def __init__(self):
        super().__init__()
        Thread.__init__(self)
        print("Initializing Eye Controller...")
        self.host='127.0.0.1'
        self.port=65432 #might as well use what PaulZC did (not sure I'll send same data yet though)
        self.shared={"curX":-1,"curY":-1,"pupil":-1,"nolid":1} #negative one means no override, current state of command to eye
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.settimeout(0.01)
        self.sock.connect_ex((self.host,self.port))
        self.face_cascade = cv2.CascadeClassifier('/home/pi/autoeye/haarcascade_frontalface_default.xml')
        self.fx=None
        self.fy=None
        self.avg=None
        self.sockLock=Lock() #lock ensures only one transmission to eye at once
        self.counterLock=Lock() #lock for determining that we have waiters for the frame
        self.frameWaiters=0
        self.frameAvail=Condition() #condition for providing or waiting for frames
        self.lastFrame=None #where we handoff frames from thread to thread
        self.last_call=0 #last time a frame was requested
        self.frame_count=0

    def run(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (1280,1024)
            #let camera warm up
            time.sleep(2)
            print("Starting to process frames...")
            while True:
                stream = io.BytesIO()
                camera.capture(stream,format='jpeg',use_video_port=False)
                buff = numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8)
                frame = cv2.imdecode(buff, 1)
                self.process_frame_difs(frame)
                #print("waiters="+str(self.frameWaiters))
                dif=time.time()-self.last_call
                if (dif)<10:
                    with self.frameAvail:
                        self.lastFrame=cv2.imencode('.jpg', frame)[1].tobytes()
                        self.frame_count+=1
                        self.frameAvail.notifyAll()
                        print("Delivered frame")
                    print("last call within "+str(int(dif))+" seconds, frame count="+str(self.frame_count))
                else:
                    print("Not delivering frame -- no one watching")
    
    def frames(self):
        self.last_call=time.time()
        #last_count=0
        while True:
            #if self.frame_count()>last_count:
            #    last_count=self.frame_count()
            with self.frameAvail: #get a lock to check for frame
                if self.lastFrame!=None:
                    yield self.lastFrame #if there is a frame yield it (could be same frame if we are too fast)
                    self.last_call=time.time()
                else:
                    time.sleep(1) #don't spin if not frame yet
    
    def aim(self,x,y):
        if self.sock!=None:
            with self.sockLock:
                bnds={"left":316,"right":916,"top":76,"bottom":694}
                self.focus(x,y)
                if x<bnds['left']:
                    self.shared['curX']=0.0
                elif x>bnds['right']:
                    self.shared['curX']=1.0
                else:
                    self.shared['curX']=(x-bnds['left'])/(bnds['right']-bnds['left'])
                    if y<bnds['top']:
                        self.shared['curY']=1.0
                    elif y>bnds['bottom']:
                        self.shared['curY']=0.0
                    else:
                        self.shared['curY']=1.0-((y-bnds['top'])/(bnds['bottom']-bnds['top']))
                self.sock.send(pickle.dumps(self.shared))
                
    def pupil(self,p):
        if self.sock!=None:
            with self.sockLock:
                self.shared['pupil']=float(p)
                self.sock.send(pickle.dumps(self.shared))
                
    def bound(self,bnd):
        if self.sock!=None:
            with self.sockLock:
                if bnd=='left':
                    self.shared['curX']=0.0
                    self.shared['curY']=0.5
                elif bnd=='right':
                    self.shared['curX']=1.0
                    self.shared['curY']=0.5
                elif bnd=='top':
                    self.shared['curX']=0.5
                    self.shared['curY']=1.0
                elif bnd=='bottom':
                    self.shared['curX']=0.5
                    self.shared['curY']=0.0
                self.sock.send(pickle.dumps(self.shared))

    def reset(self):
        if self.sock!=None:
            with self.sockLock:
                self.shared['curX']=-1
                self.shared['curY']=-1
                self.shared['pupil']=-1
                self.shared['nolid']=1 #nolid is default
                self.focus(None,None)
                self.sock.send(pickle.dumps(self.shared))

    def toggleLid(self):
        if self.sock!=None:
            with self.sockLock:
                if self.shared['nolid']==-1:
                    self.shared['nolid']=1
                elif self.shared['nolid']==1:
                    self.shared['nolid']=-1
                self.sock.send(pickle.dumps(self.shared))

    def focus(self,x,y):
        self.fx=x
        self.fy=y

    def process_frame_face(self,frame):
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5)
        if len(faces)>0:
            print("Faces at:")
            for (x,y,w,h) in faces:
                print("  "+str(x)+","+str(y)+","+str(w)+","+str(h))
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
            #Draw a rectangle around every found face
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
        else:
            print("No faces")
        if self.fx!=None and self.fy!=None:
            cv2.circle(frame,(int(self.fx),int(self.fy)),10,(0,0,255),2)
            
    def process_frame_difs(self,frame):
        #frame = imutils.resize(origframe, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # if the average frame is None, initialize it
        if self.avg is None:
            print("[INFO] starting background model...")
            self.avg = gray.copy().astype("float")
            return
        # accumulate the weighted average between the current frame and
        # previous frames, then compute the difference between the current
        # frame and running average
        cv2.accumulateWeighted(gray, self.avg, 0.5)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(self.avg))
        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        thresh = cv2.threshold(frameDelta, 5, 255,cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # loop over the contours
        cont=None
        cont_size=0
        for c in cnts:
                # if the contour is too small, ignore it
                sz=cv2.contourArea(c)
                #print("size="+str(sz))
                if sz < 500:
                        continue
                if sz>cont_size:
                    cont=c
                    cont_size=sz
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                #print("rect=",x,y,w,h)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        if cont_size>0:
                (x, y, w, h) = cv2.boundingRect(cont)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                self.aim(x+w/2,y+h/2)
        # display the image
        if self.fx!=None and self.fy!=None:
                cv2.circle(frame,(int(self.fx),int(self.fy)),10,(0,0,255),2)

