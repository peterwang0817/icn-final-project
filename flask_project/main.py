import os
import cv2
from shutil import copyfile

from flask import Flask, render_template, Response
from stream_client import Client

app = Flask(__name__)

SERVER_ADDRESS = '127.0.0.1'
SERVER_RTSP_PORT = 554
CLIENT_RTP_PORT = 25000

video_capture = cv2.VideoCapture(0)
foo = Client('movie.Mjpeg', SERVER_ADDRESS, SERVER_RTSP_PORT, CLIENT_RTP_PORT)
copyfile('static/default.jpg', 't.jpg')

def gen():
    while True:
        '''
        ret, image = video_capture.read()
        cv2.imwrite('t.jpg', image)
        '''
        #'''        
        #'''
        cache_filename = 'cache{0}.jpg'.format(foo.session_id)
        if not os.path.isfile(cache_filename):
            cache_filename = 'static/default.jpg'
        else:
            copyfile(cache_filename, 't.jpg')
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')
        #yield (b'--frame\r\n'
            #b'Content-Type: image/jpeg\r\n\r\n' + open(cache_filename, 'rb').read() + b'\r\n')
        #'''
        
    video_capture.release()

@app.route('/')
def index():
    """Video streaming"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/setup')
def setup():
    foo.setup()
    print('setup')
    return 'setup'

@app.route('/play')
def play():
    foo.play()
    print('play')
    return 'play'

@app.route('/pause')
def pause():
    foo.pause()
    print('pause')
    return 'pause'

@app.route('/teardown')
def teardown():
    foo.teardown()
    print('teardown')
    return 'teardown'

if __name__ == '__main__':
    app.run()