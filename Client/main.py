from flask import Flask, render_template, Response
from video_client import VideoClient
from audio_client import AudioClient
import sys

app = Flask(__name__)

SERVER_ADDRESS = '127.0.0.1'
SERVER_RTSP_PORT = 554
CLIENT_RTP_PORTS = (25000, 25001)




@app.route('/')
def index():
    """Video streaming"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    def gen_video():
        while True:
            if foo.current_video_frame != None:
                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + foo.current_video_frame + b'\r\n')
            else:
                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + open('static/default.jpg', 'rb').read() + b'\r\n')

    return Response(gen_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/audio_feed')
def audio_feed():
    def gen_audio():
        while True:
            if foo.current_audio != None:
                yield #(b'--frame\r\nContent-Type: audio/x-wav\r\n\r\n' + foo.current_audio + b'\r\n')

    return Response(gen_audio(), mimetype='audio/x-wav')

@app.route('/setup')
def setup():
    foo.setup()
    bar.setup()
    print('setup')
    return 'setup'

@app.route('/play')
def play():
    foo.play()
    bar.play()
    print('play')
    return 'play'

@app.route('/pause')
def pause():
    foo.pause()
    bar.pause()
    print('pause')
    return 'pause'

@app.route('/teardown')
def teardown():
    foo.teardown()
    bar.teardown()
    print('teardown')
    return 'teardown'

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == "video":
        foo = VideoClient('./data/movie.mp4', SERVER_ADDRESS, SERVER_RTSP_PORT, CLIENT_RTP_PORTS[0])
        bar = AudioClient('./data/movie.wav', SERVER_ADDRESS, SERVER_RTSP_PORT, CLIENT_RTP_PORTS[1])
    elif mode == "meet":
        foo = VideoClient('LIVE', SERVER_ADDRESS, SERVER_RTSP_PORT, CLIENT_RTP_PORTS[0])
        bar = AudioClient('MICRO', SERVER_ADDRESS, SERVER_RTSP_PORT, CLIENT_RTP_PORTS[1])
    else:
        print("Invalid mode, choose from video or meet")
        raise ValueError
    app.run()