#find solutions for golf packing puzzle -- Scott Bennett -- 7/29/19

pieces=[
    ['p1',1,0,0,1,-1,-1],
    ['p2',1,0,-1,-1,-1,-1],
    ['p3',1,0,1,0,0,1],
    ['p4',-1,-1,0,1,1,0],
    ['p5',1,0,0,1,1,0],
    ['p6',1,0,-1,-1,0,1],
]

def possibles(top,used):
    result=[]
    for piece in pieces:
        if piece[0] not in used:
            result.extend(possibles2(top,piece))
    return(result)

def contains(x,y):
    for i in y:
        if (i[0]==x[0] and i[1]==x[1] and i[2]==x[2] and i[3]==x[3]):
            return(True)
    return(False)

def possibles2(t,p):
    result=[]
    if (((t[0]+p[1])<=0) and ((t[1]+p[3])<=0) and ((t[2]+p[5])<=0)):
        result.append([p[0],p[2],p[4],p[6]])
    if (((t[0]+p[2])<=0) and ((t[1]+p[4])<=0) and ((t[2]+p[6])<=0)):
        result.append([p[0],p[1],p[3],p[5]])
    if (((t[0]+p[6])<=0) and ((t[1]+p[4])<=0) and ((t[2]+p[2])<=0)):
        result.append([p[0],p[5],p[3],p[1]])
    if (((t[0]+p[5])<=0) and ((t[1]+p[3])<=0) and ((t[2]+p[1])<=0)):
        result.append([p[0],p[6],p[4],p[2]])
    result2=[]
    for x in result:
        if not contains(x,result2):
            result2.append(x)
    return(result2)

def next(b):
    if (len(b)<3):
        return([-1,-1,-1]) #filling the first 3 rows
    elif (len(b)<6):
        return([b[0][len(b)-2],b[1][len(b)-2],b[2][len(b)-2]]) #filling the next 3 columns
    else:
        return(None) #done

def solve(board,used):
    global solutions
    nxt=next(board)
    #print("board:"+str(board)+" used:"+str(used)+" next:"+str(nxt))
    if (nxt==None):
        solutions.append(board)
        return(None)
        #return(board)
    for x in possibles(nxt,used):
        result=solve(board+[x],used+[x[0]])
        if (result!=None):
            return(result)
    return(None)

solutions=[]
print(solve([],[]))
s=1
for x in range(len(solutions)):
    print(str(s)+": "+str(solutions[x]))
    s=s+1

