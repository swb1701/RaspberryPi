#!/usr/bin/env python
from flask import Flask, render_template, Response, request, json, jsonify
from eye_controller import EyeController

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(eye):
    for frame in eye.frames():
    #while True:
    #frame = eye.frames()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(eye),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pupil',methods=['GET','POST'])
def pupil():
    p=request.form['pupil']
    eye.pupil(p)
    return jsonify({'rc':'OK'})

@app.route('/pos',methods=['GET','POST'])
def pos():
    x=float(request.form['x'])
    y=float(request.form['y'])
    eye.aim(x,y)
    return jsonify({'rc':'OK'})

@app.route('/bound',methods=['GET','POST'])
def bound():
    bound=request.form['bound']
    eye.bound(bound)
    return jsonify({'rc':'OK'})

@app.route('/reset',methods=['GET','POST'])
def reset():
    eye.reset()
    return jsonify({'rc':'OK'})

@app.route('/toggleLid',methods=['GET','POST'])
def toggleLid():
    eye.toggleLid()
    return jsonify({'rc':'OK'})

if __name__ == '__main__':
    eye=EyeController()
    eye.start()
    app.run(host='0.0.0.0', threaded=True)
