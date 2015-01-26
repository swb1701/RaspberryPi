timelapse.py runs on the PI capturing a photo every 2 minutes and uploading to Amazon S3

timelapse-download.py will recursively download the photos from S3 and sequentially name them to prepare for creating a movie

condense.py was used to re-sequence the files after excluding those which were taken in darkness

An example video produced using this code is at: https://www.youtube.com/watch?v=CwldvVFiF6A&feature=youtu.be