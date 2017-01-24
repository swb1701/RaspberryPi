import Part
from FreeCAD import Base

#Pattern for Lasercut LED Tree
#Scott Bennett, 01/17

baseWidth=160
treeHeight=1.618*baseWidth #golden ratio
ringWidth=6
topRingWidth=12
thickness=3.175
rings=[16,36,56,76,96,baseWidth-ringWidth]

def pt(pts,x,y,flip):
    if flip:
        x=x+baseWidth*0.6
        y=treeHeight-(y-50)+50
    pts.append(Base.Vector(x,y,0))

def tree(ulx,uly,flip=False):
    treeparts=len(rings)
    partHeight=treeHeight/treeparts
    partWidth=baseWidth/2/treeparts
    x=ulx+baseWidth/2
    y=uly
    pts=[]
    if not flip:
        pt(pts,x-thickness/2,y,flip)
	pt(pts,x-thickness/2,y+treeHeight/2,flip)
	pt(pts,x+thickness/2,y+treeHeight/2,flip)
	pt(pts,x+thickness/2,y,flip)
    else:
	pt(pts,x,y,flip)
    pt(pts,x+topRingWidth/2,y,flip)
    for i in range(treeparts):
        pt(pts,x+rings[i]/2,y+partHeight*(i+1),flip)
	if i<(treeparts-1):
	    pt(pts,x+rings[i]/2+ringWidth,y+partHeight*(i+1),flip)
	if i<(treeparts-2):
	    pt(pts,x+rings[i]/2+ringWidth,y+partHeight*(i+1)+partHeight*0.2,flip)
	    pt(pts,x+thickness*2*(i+1),y+partHeight*(i+1)+partHeight*0.1,flip)
    if flip:
        pt(pts,x+thickness/2,y+partHeight*treeparts,flip)
	pt(pts,x+thickness/2,y+treeHeight/2,flip)
	pt(pts,x-thickness/2,y+treeHeight/2,flip)
	pt(pts,x-thickness/2,y+partHeight*treeparts,flip)
    for i in range(treeparts-1,-1,-1):
        if i<(treeparts-2):
	    pt(pts,x-thickness*2*(i+1),y+partHeight*(i+1)+partHeight*0.1,flip)
	    pt(pts,x-rings[i]/2-ringWidth,y+partHeight*(i+1)+partHeight*0.2,flip)
	if i<(treeparts-1):
	    pt(pts,x-rings[i]/2-ringWidth,y+partHeight*(i+1),flip)
	pt(pts,x-rings[i]/2,y+partHeight*(i+1),flip)
    pt(pts,x-topRingWidth/2,y,flip)
    if flip:
        pt(pts,x,y,flip)
    else:
        pt(pts,x-thickness/2,y,flip)
    return(pts)

pts=tree(0,50,False)
poly=Part.makePolygon(pts)
Part.show(poly)
pts=tree(0,50,True)
poly=Part.makePolygon(pts)
Part.show(poly)
