from Tkinter import *
import math

class Piece:

    def __init__(self, canvas, pts, color, name, ulx, uly):
        self.canvas=canvas
        self.pts=pts
        self.ulx=ulx
        self.uly=uly
        self.grid=30
        self.color=color
        self.name=name

    #draw the piece at grid x,y
    def draw(self,x,y):
        #print(self.pts)
        bb=self.bbox()
        #print(bb)
        for p in self.pts:
            pulx=(x+p[0]-bb['x'])*self.grid
            puly=(y-p[1]+bb['y'])*self.grid
            self.canvas.create_rectangle((self.ulx+pulx,self.uly+puly,self.ulx+pulx+self.grid,self.uly+puly+self.grid),fill=self.color)

    def draw_at_pt(self,x,y):
        #print(self.pts)
        bb=self.bbox()
        #print(bb)
        for p in self.pts:
            pulx=(0+p[0]-bb['x'])*self.grid
            puly=(0-p[1]+bb['y'])*self.grid
            self.canvas.create_rectangle((x+pulx,y+puly,x+pulx+self.grid,y+puly+self.grid),fill=self.color)

    #get bounding box for this piece
    def bbox(self):
        return(self.bbox_pts(self.pts))

    #get bounding box for pts
    def bbox_pts(self,pts):
        minx=pts[0][0]
        maxx=pts[0][0]
        miny=pts[1][1]
        maxy=pts[1][1]
        for p in pts:
            if p[0]<minx:
                minx=p[0]
            if p[0]>maxx:
                maxx=p[0]
            if p[1]<miny:
                miny=p[1]
            if p[1]>maxy:
                maxy=p[1]
        result={}
        result['x']=minx
        result['y']=miny
        result['w']=maxx-minx+1
        result['h']=maxy-miny+1
        return(result)

    #flip pts about y axis
    def flip_pts(self,pts):
        npts=[]
        for p in pts:
            npts.append((-1*p[0],p[1]))
        return(npts)

    #rotate pts at angle (should be multiple of 90)
    def rotate_pts(self,pts,angle):
        npts=[]
        angle=math.radians(angle)
        for p in pts:
            npts.append((round(math.cos(angle)*p[0]-math.sin(angle)*p[1]),round(math.sin(angle)*p[0]+math.cos(angle)*p[1])))
        return(npts)

    #test if pts1 and pts2 are the same shape and orientation
    def same_pts(self,pts1,pts2):
        bb1=self.bbox_pts(pts1)
        bb2=self.bbox_pts(pts2)
        #print(pts1)
        #print(bb1)
        #print(pts2)
        #print(bb2)
        for p in pts2:
            cp=(p[0]-bb2['x']+bb1['x'],p[1]-bb2['y']+bb1['y'])
            #print(str(cp)+" vs. "+str(pts1))
            if (cp not in pts1):
                #print("False")
                return(False)
        #print("True")
        return(True)

    #return True if flipping the shape results in the same shape and False otherwise
    def noflip(self):
        fpts=self.flip_pts(self.pts)
        for i in range(4):
            #print("angle="+str(i*90))
            if self.same_pts(fpts,self.rotate_pts(self.pts,90*i)):
                return(True)
        return(False)

    #flip the piece about the Y axis
    def flip(self):
        self.pts=self.flip_pts(self.pts)

    def flip_copy(self):    
        npts=self.flip_pts(self.pts)
        return(Piece(self.canvas,npts,self.color,self.name,self.ulx,self.uly))

    #rotate the piece by angle (multiple of 90)
    def rotate(self,angle):
        self.pts=self.rotate_pts(self.pts,angle)

    def rotate_copy(self,angle):
        npts=self.rotate_pts(self.pts,angle)
        return(Piece(self.canvas,npts,self.color,self.name,self.ulx,self.uly))

    #check if this piece is the same as pts
    def same(self,pts):
        return(self.same_pts(pts,self.pts))
