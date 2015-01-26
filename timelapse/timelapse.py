#!/usr/bin/python
#
# TimeLapse Photo Sender to S3
#

import time
import boto
import subprocess
from boto.s3.key import Key

#get access to S3
conn=boto.connect_s3('access_key','secret_key')
#our bucket name
bucketname='plant-photos'
#our default capture filename
filename='plant.jpg'
#get access to bucket
bucket=conn.get_bucket(bucketname)
i=0
while True:
  #capture frame
  p=subprocess.Popen(["raspistill","-o",filename],bufsize=2048,stdin=subprocess.PIPE,stdout=subprocess.PIPE,close_fds=True)
  p.wait()
  #set up the key
  k=Key(bucket)
  t=time.strftime('%y/%m/%d/%H/%y%m%d-%H%M%S.jpg')
  print("Took Photo:"+t)
  k.key=t
  i=i+1
  #transfer the file
  k.set_contents_from_filename(filename)
  #wait 2 minutes
  time.sleep(2*60)
