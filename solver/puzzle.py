from Tkinter import *
import math

class Puzzle:

    def __init__(self, name, boundary_mm, pieces, square_mm):
        self.boundary_mm=boundary_mm
        self.pieces=pieces
        self.square_mm=square_mm
        self.area=0
        for piece in pieces:
            self.area=self.area+len(piece.pts)
        self.name=name
        print(name+" area="+str(self.area))

    def draw(self,canvas,x,y,width,height):
        canvas.create_rectangle([x,y,x+width,y+height],fill='brown')
        
