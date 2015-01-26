import os
from subprocess import call
i=0
for fn in sorted(os.listdir('images')):
    if fn.endswith(".jpg"):
        print fn
        call(["ln",'images/'+fn,'images2/'+str(i).zfill(6)+'.jpg'])
        i=i+1
