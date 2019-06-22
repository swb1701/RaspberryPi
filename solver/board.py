from Tkinter import *
import math
import copy
from piece import Piece

class Board:

    def __init__(self, canvas, w, h, grid, ulx, uly, occupied):
        self.canvas=canvas
        self.w=w
        self.h=h
        self.ulx=ulx
        self.uly=uly
        self.grid=grid
        self.pieces=[]
        self.occupied=occupied

    def copy_state(self,pieces):
        self.pieces=copy.copy(pieces)

    def area(self):
        result=0
        for i in range(len(self.occupied)):
            for j in range(len(self.occupied[0])):
              if self.occupied[i][j]==0:
                  result=result+1
        return(result)

    def dup(self):
        nb=Board(self.canvas,self.w,self.h,self.grid,self.ulx,self.uly,copy.deepcopy(self.occupied))
        nb.copy_state(self.pieces)
        return(nb)

    def add(self,piece,x,y):
        bb=piece.bbox() #bounding box for piece
        for p in piece.pts: #check for collisions
            ulx=int(x+p[0]-bb['x'])
            uly=int(y-p[1]+bb['y'])
            if (self.occupied[uly][ulx]!=0):
                return(False) #reject if occupied
        self.pieces.append((piece,x,y)) #record the piece
        for p in piece.pts:
            ulx=int(x+p[0]-bb['x'])
            uly=int(y-p[1]+bb['y'])
            self.occupied[uly][ulx]=piece.name #mark occupied
        #print(str(self.occupied)) #show updated board
        return(True)

    def draw(self):
        self.canvas.create_rectangle((self.ulx,self.uly,self.w*self.grid+self.ulx,self.h*self.grid+self.uly))
        for p in self.pieces:
            p[0].draw(p[1],p[2])
