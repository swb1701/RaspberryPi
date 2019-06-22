#Disection Puzzle Solver, Scott Bennett, 6/2019 (Work in Progress)
from Tkinter import *
import math
import time
import copy
from piece import Piece
from board import Board
from puzzle import Puzzle

master=Tk()
w=1000 #set the width of our canvas
h=1000 #set the hieght of our canvas
grid=60
white=(255,255,255)
canvas=Canvas(master,width=w,height=h)

def key(event):
    global slide_x,slide_y,occupied,puzzle,canvas,board,rotate_around,cur_puzzle,solncnt
    #canvas=event.widget.canvas
    #print "Pressed:",event.keycode
    redraw=1
    if (event.keycode==37): #left
        #print("Left")
        slide_x=slide_x-1
    elif (event.keycode==38): #up
        #print("Up")
        slide_y=slide_y+1
    elif (event.keycode==39): #right
        #print("Right")
        slide_x=slide_x+1
    elif (event.keycode==40): #down
        #print("Down")
        slide_y=slide_y-1
    elif (event.keycode==82): #r
        #print("Rotate")
        rotate_around=rotate_around+1
        if (rotate_around>(len(puzzle.boundary_mm)-1)*2):
            rotate_around=0
    elif (event.keycode==83): #s
        canvas.delete(ALL)        
        puzzle.boundary_mm=rotate_boundary()    
        occupied=intersect_grid()
        #print(occupied)
        board=Board(canvas,sizew,sizeh,grid,ulx,uly,occupied)
        canvas.update()
        if board.area()<puzzle.area:
            print("Not enough squares to solve")
        else:
            solncnt=0
            print(solve(board,puzzle.pieces))
        redraw=0
    elif (event.keycode==78): #n
        cur_puzzle=cur_puzzle+1
        if (cur_puzzle>(len(puzzles)-1)):
            cur_puzzle=0
        puzzle=puzzles[cur_puzzle]
        puzzle.boundary_mm=copy.deepcopy(puzzle.boundary_mm)
    elif (event.keycode==80): #p
        cur_puzzle=cur_puzzle-1
        if (cur_puzzle<0):
            cur_puzzle=len(puzzles)-1
        puzzle=puzzles[cur_puzzle]
        puzzle.boundary_mm=copy.deepcopy(puzzle.boundary_mm)
    if redraw==1:
        canvas.delete(ALL)        
        puzzle.boundary_mm=rotate_boundary()    
        occupied=intersect_grid()
        print(occupied)
        board=Board(canvas,sizew,sizeh,grid,ulx,uly,occupied)
        canvas.update()
        if board.area()<puzzle.area:
            print("Not enough squares ("+str(board.area())+") to solve -- needs "+str(puzzle.area))
        else:
            print("You have enough squares ("+str(board.area())+"), hit 's' if you want to attempt a solution")

def callback(event):
    canvas.focus_set()
    #print "Clicked At:",event.x,event.y

canvas.bind("<Key>",key)
canvas.bind("<Button-1>",callback)
canvas.pack()

border=2

puzzles=[]
cur_puzzle=0

#maximum possible tile bounds
sizew=8
sizeh=7

ulx=(w-sizew*grid)/2
uly=(h-sizeh*grid)/2

#convention: 0,0 will be bottom left most tile of piece

#actual_square_mm=15.4
slide_x=grid-10
slide_y=0
rotate_around=0
#boundary_mm=[(0,0),(120,0),(90,90),(30,90)] #trapezoid
#boundary_mm=[(0,0),(90,30),(90,90),(0,120)] #trapezoid

#pieces=[
#    Piece(canvas,[(0,0),(1,0),(2,0),(1,1)],"red",1,ulx,uly),
#    Piece(canvas,[(0,0),(1,0),(2,0),(2,1),(3,1)],"green",2,ulx,uly),
#    Piece(canvas,[(0,0),(1,0),(1,1),(1,2),(2,1)],"light blue",3,ulx,uly),
#    Piece(canvas,[(0,0),(1,0),(1,1),(1,2),(2,1)],"yellow",4,ulx,uly),
#    Piece(canvas,[(0,0),(1,0),(1,1),(2,1),(2,2)],"orange",5,ulx,uly)
#]

puzzles.append(Puzzle("Martin's Menace",
                      [(0,0),(90,0),(90,76),(0,76)],
                      [
                          Piece(canvas,[(0,0),(1,0),(1,1),(1,2),(2,2)],"red",1,ulx,uly),
                          Piece(canvas,[(0,0),(1,0),(1,1),(2,0),(3,0)],"green",2,ulx,uly),
                          Piece(canvas,[(0,0),(1,0),(1,1),(1,2),(2,1)],"light blue",3,ulx,uly),
                          Piece(canvas,[(0,0),(1,0),(1,1),(1,2),(2,0)],"yellow",4,ulx,uly)
                          ],
                      15.8))

puzzles.append(Puzzle("Basket Case",
                     [(0,0),(120,0),(90,90),(30,90)],
                     [
                         Piece(canvas,[(0,0),(1,0),(2,0),(1,1)],"red",1,ulx,uly),
                         Piece(canvas,[(0,0),(1,0),(2,0),(2,1),(3,1)],"green",2,ulx,uly),
                         Piece(canvas,[(0,0),(1,0),(1,1),(1,2),(2,1)],"light blue",3,ulx,uly),
                         Piece(canvas,[(0,0),(1,0),(1,1),(1,2),(2,1)],"yellow",4,ulx,uly),
                         Piece(canvas,[(0,0),(1,0),(1,1),(2,1),(2,2)],"orange",5,ulx,uly)
                         ],
                     14.9))
puzzles.append(Puzzle("Castle1",
                      [(0,0),(77.78,0),(77.78,23.33),(39,62.22),(0,23.33)],
                      [
                          Piece(canvas,[(0,0),(1,0),(2,0),(2,1),(3,0)],"red",1,ulx,uly),
                          Piece(canvas,[(0,0),(0,1),(1,1),(2,1)],"green",2,ulx,uly),
                          Piece(canvas,[(0,0),(0,1),(1,0),(1,1),(2,1)],"light blue",3,ulx,uly),
                          Piece(canvas,[(0,0),(1,0),(1,1),(2,1),(3,1)],"yellow",4,ulx,uly),
                          Piece(canvas,[(0,0),(1,0),(1,1),(1,2),(2,1)],"orange",5,ulx,uly)
                          ],
                      10.6))
puzzles.append(Puzzle("Castle2",
                      [(0,0),(33,0),(33,-11),(44,-11),(44,0),(77,0),(77,22),(38.5,60),(0,22)],
                      [
                          Piece(canvas,[(0,0),(1,0),(2,0),(2,1),(3,0)],"red",1,ulx,uly),
                          Piece(canvas,[(0,0),(0,1),(1,1),(2,1)],"green",2,ulx,uly),
                          Piece(canvas,[(0,0),(0,1),(1,0),(1,1),(2,1)],"light blue",3,ulx,uly),
                          Piece(canvas,[(0,0),(1,0),(1,1),(2,1),(3,1)],"yellow",4,ulx,uly),
                          Piece(canvas,[(0,0),(1,0),(1,1),(1,2),(2,1)],"orange",5,ulx,uly)
                          ],
                      10.6))
puzzles.append(Puzzle("Castle3",
                      [(0,0),(77,0),(77,22),(44,55),(44,66),(33,66),(33,55),(0,22)],
                      [
                          Piece(canvas,[(0,0),(1,0),(2,0),(2,1),(3,0)],"red",1,ulx,uly),
                          Piece(canvas,[(0,0),(0,1),(1,1),(2,1)],"green",2,ulx,uly),
                          Piece(canvas,[(0,0),(0,1),(1,0),(1,1),(2,1)],"light blue",3,ulx,uly),
                          Piece(canvas,[(0,0),(1,0),(1,1),(2,1),(3,1)],"yellow",4,ulx,uly),
                          Piece(canvas,[(0,0),(1,0),(1,1),(1,2),(2,1)],"orange",5,ulx,uly)
                          ],
                      10.6))

puzzle=puzzles[cur_puzzle]
puzzle.boundary_mm=copy.deepcopy(puzzle.boundary_mm)

#canvas.create_rectangle((border,border,sizew*grid+border,sizeh*grid+border))

#cx=0
#cy=(h/grid)-1
#for p in pieces:
#    p.draw(cx,cy)
#    bb=p.bbox()
#    cx=cx+bb['w']
#    cy=cy-bb['h']

#canvas.update()

#print("same1="+str(pieces[0].same(pieces[0].pts))) #True
#print("same2="+str(pieces[0].same(pieces[1].pts))) #False
#print("same3="+str(pieces[0].same(pieces[0].rotate_pts(pieces[0].pts,90)))) #False
#print("same4="+str(pieces[0].same(pieces[0].flip_pts(pieces[0].pts)))) #True

#for i in range(len(pieces)):
#    print(str(i)+':'+str(pieces[i].noflip()))

def rotate_boundary():
    rot=rotate_around/2
    extra=rotate_around%2
    pt=puzzle.boundary_mm[rot] #rotate about second point
    nxt=rot+1
    if (nxt>(len(puzzle.boundary_mm)-1)):
        nxt=0
    pt2=puzzle.boundary_mm[nxt] #second point to be on baseline
    angle=math.atan2(pt2[1]-pt[1],pt2[0]-pt[0])
    #print("pts="+str(pt)+" "+str(pt2))
    #print("angle="+str(angle))
    npts=[]
    for p in puzzle.boundary_mm:
        npts.append((p[0]-pt[0],p[1]-pt[1]))
    angle=-1*angle
    if (extra==1):
        angle=angle+(3.1415/4.0)
    npts2=[]
    for p in npts:
        npts2.append((round(math.cos(angle)*p[0]-math.sin(angle)*p[1])+slide_x,slide_y+round(math.sin(angle)*p[0]+math.cos(angle)*p[1])))
    return(npts2)

def draw_boundary():
    global canvas
    scale=1.0*grid/puzzle.square_mm
    pts=[]
    for i in range(len(puzzle.boundary_mm)):
        p=puzzle.boundary_mm[i]
        pts.append(int(ulx+p[0]*scale))
        pts.append(int(uly+sizeh*grid-p[1]*scale))
    print(pts)
    canvas.create_polygon(pts,outline='red',fill='')

def intersect_grid():
    global canvas
    canvas.create_text(20,20,anchor='nw',text='Puzzle: '+puzzle.name,font="Times 20 italic bold")
    for i in range(len(puzzle.pieces)):
        piece=puzzle.pieces[i]
        piece.draw_at_pt(i*150+50,150)
    puzzle.draw(canvas,700,50,250,125)
    scale=1.0*grid/puzzle.square_mm
    pts=[]
    pts2=[]
    occupied=[]
    for i in range(sizeh):
        lst=[]
        for j in range(sizew):
            lst.append(0)
        occupied.append(lst)
    for i in range(len(puzzle.boundary_mm)):
        p=puzzle.boundary_mm[i]
        x=int(ulx+p[0]*scale)
        y=int(uly+sizeh*grid-p[1]*scale)
        pts.append(x)
        pts.append(y)
        pts2.append([x,y])
    for row in range(sizeh):
        for col in range(sizew):
            rect=[ulx+col*grid,uly+row*grid,ulx+col*grid+grid,uly+row*grid+grid]
            if rect_inside_poly(rect,pts2):
               canvas.create_rectangle(rect,outline='black',fill='green')
            else:
               canvas.create_rectangle(rect,outline='black',fill='red')
               #canvas.create_line([rect[0],rect[1],rect[2],rect[3]],fill='black')
               #canvas.create_line([rect[2],rect[1],rect[0],rect[3]],fill='black')
               occupied[row][col]='X'
    canvas.create_polygon(pts,outline='blue',fill='')
    return(occupied)

def rect_inside_poly(r,poly):
    if not point_in_poly(r[0],r[1],poly):
        return(False)
    if not point_in_poly(r[2],r[1],poly):
        return(False)
    if not point_in_poly(r[0],r[3],poly):
        return(False)
    if not point_in_poly(r[2],r[3],poly):
        return(False)
    return(True)
    
# https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python   
def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside
    
def showpos():
    global canvas
    for p in puzzle.pieces:
        for f in range(2):
            if (f==1 and p.noflip()):
                break
            else:
                p.flip()
            for i in range(4):
                p.rotate(90*i)
                bb=p.bbox()
                for x in range(sizew-int(bb['w'])+1):
                    for y in range(sizeh-int(bb['h'])+1):
                        canvas.delete("all")
                        canvas.create_rectangle((border,border,sizew*grid+border,sizeh*grid+border))
                        #canvas.create_rectangle((border+x*grid,border+y*grid,border+x*grid+bb['w']*grid,border+y*grid+bb['h']*grid))
                        p.draw(x,y+bb['h']-1)
                        canvas.update()
                        time.sleep(0.1)

def animate():
    global canvas
    while True:
        canvas.delete("all")
        cx=0
        cy=(h/grid)-1
        for p in puzzle.pieces:
            p.rotate(90)
            p.draw(cx,cy)
            bb=p.bbox()
            cx=cx+bb['w']
            cy=cy-bb['h']
        canvas.update()
        time.sleep(1)

canvas.delete("all")        

def solve(board,pieces):
    global solncnt
    if (solncnt>0):
        return([]) #for testing
    if len(pieces)==0:
        solncnt=solncnt+1
        print("Solution #"+str(solncnt)+" Found")
        if (solncnt==1):
            canvas.delete("all")
            board.draw()
            #draw_boundary()
            print(intersect_grid())
            canvas.update()
        return([board])
    else:
        solns=[]
        p=pieces[0]
        for f in range(2):
            if (f==1 and p.noflip()):
                break
            else:
                p=p.flip_copy()
            for i in range(4):
                p=p.rotate_copy(90*i)
                bb=p.bbox()
                for x in range(sizew-int(bb['w'])+1):
                    for y in range(sizeh-int(bb['h'])+1):
                        nb=board.dup()
                        if nb.add(p,x,y+bb['h']-1):
                            solns=solns+solve(nb,pieces[1:])
                        #else:
                            #print("Can't place "+str(p.name)+" "+str(f)+":"+str(i)+":"+str(x)+":"+str(y))
        #print("end of solve with "+str(len(pieces))+" left -- board is "+str(board.occupied))
        return(solns)

puzzle.boundary_mm=rotate_boundary()    
solncnt=0
occupied=intersect_grid()
canvas.update()
board=Board(canvas,sizew,sizeh,grid,ulx,uly,occupied)
#print(solve(board,puzzle.pieces))
    
#master.after(0,animate)
#master.after(0,showpos())
master.mainloop() #main loop
