#flap control using multiple flag groups, multi-processing
from multiprocessing import Process
from flapgroup import FlapGroup

#fghi=FlapGroup(0x20)
#fglo=FlapGroup(0x21)

#fghi.setDigit(0,5, 0x00F0,26+13)
#fghi.setDigit(1,6, 0x000F,26)
#fghi.setDigit(2,13,0xF000,26+8)
#fghi.setDigit(3,19,0x0F00,26+26)
#fglo.setDigit(0,22,0x000F,13+4)
#fglo.setDigit(1,27,0x00F0,39+4)
#fglo.setDigit(2,17,0x0F00,13)
#fglo.setDigit(3,4, 0xF000,4)

#print(fghi)
#print(fglo)

#sequential test of 2 flapgroups
#def display(word):
#    fghi.display(word[0:4])
#    fglo.display(word[4:8])

def display1(word):
    fg=FlapGroup(0x20)
    fg.setDigit(0,5, 0x00F0,26+4)
    fg.setDigit(1,6, 0x000F,26)
    fg.setDigit(2,13,0xF000,26+4)
    fg.setDigit(3,19,0x0F00,26+8)
    fg.display(word)
    
def display2(word):
    fg=FlapGroup(0x21)
    fg.setDigit(0,22,0x000F,13+4)
    fg.setDigit(1,27,0x00F0,39+4)
    fg.setDigit(2,17,0x0F00,13)
    fg.setDigit(3,4, 0xF000,4)
    fg.display(word)

def pdisplay(word):
    p1=Process(target=display1,args=(word[0:4],))
    p2=Process(target=display2,args=(word[4:8],))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

#TODO: need inter-process comms to send instructions
pdisplay('        ')
pdisplay('12345678')

