from flask import Flask, render_template, Response
from stream_client import Client



app = Flask(__name__)

SERVER_ADDRESS = '127.0.0.1'
SERVER_RTSP_PORT = 554
CLIENT_RTP_PORTS = (25000, 25001)

#video_capture = cv2.VideoCapture(0)
foo = Client('movie.Mjpeg', SERVER_ADDRESS, SERVER_RTSP_PORT, CLIENT_RTP_PORTS)

def gen_video():
    while True:
        '''
        success, frame = video_capture.read()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        #cv2.imwrite('t.jpg', image)
        '''
        #'''        
        '''
        cache_filename = 'cache{0}.jpg'.format(foo.session_id)
        if not os.path.isfile(cache_filename):
            cache_filename = 'static/default.jpg'
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + open(cache_filename, 'rb').read() + b'\r\n')
        '''
        if foo.current_frame != None:
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + foo.current_frame + b'\r\n')
        else:
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + open('static/default.jpg', 'rb').read() + b'\r\n')
        #'''
        
    video_capture.release()

def gen_audio():
    while True:
        if foo.current_audio != None:
            yield (b'--frame\r\nContent-Type: audio/mp3\r\n\r\n' + foo.current_audio + b'\r\n')

@app.route('/')
def index():
    """Video streaming"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/audio_feed')
def audio_feed():
    return Response(gen_audio(), mimetype='audio/mp3')

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