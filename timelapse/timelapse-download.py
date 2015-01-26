#!/usr/bin/python
#
# TimeLapse Downloader
#

import time
import boto
import subprocess
from boto.s3.key import Key

#get access to S3
conn=boto.connect_s3('access_key','secret_key')
#our bucket name
bucketname='plant-photos'
#get access to bucket
bucket=conn.get_bucket(bucketname)
list=bucket.list()
i=0
for key in list:
  fname='images/'+str(i).zfill(6)+'.jpg'
  print fname,key.name
  ky=Key(bucket,key)
  ky.get_contents_to_filename(fname)
  i=i+1


