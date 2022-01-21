import cv2
import numpy as np
import moviepy.editor as mp
import wave
import pyaudio

class MJPEG:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.file = open(filename, 'rb')
        except:
            raise IOError
        self.frameNum = 0
        self.FPS = 1 / 0.05

    def nextFrame(self):
        """Get next frame."""
        data = self.file.read(5)  # Get the framelength from the first 5 bits
        if data:
            framelength = int(data)

            # Read the current frame
            data = self.file.read(framelength)
            self.frameNum += 1
        return data

    def frameNbr(self):
        """Get frame number."""
        return self.frameNum

    def fps(self):
        return self.FPS


class MP4:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.file = cv2.VideoCapture(filename)
            self.FPS = self.file.get(cv2.CAP_PROP_FPS)
        except:
            raise IOError
        self.framenum = 0

    def nextFrame(self):
        success, frame = self.file.read()
        if success:
            frame = cv2.resize(frame, (160, 120))
            _, buffer = cv2.imencode('.jpg', frame)
            buffer = np.array(buffer)
            frame = buffer.tobytes()

        self.framenum += 1
        return frame

    def frameNbr(self):
        return self.framenum

    def fps(self):
        return self.FPS


class CAMERA:
    def __init__(self):
        self.framenum = 0
        self.camera = cv2.VideoCapture(0)
        self.FPS = 1 / 0.03

    def nextFrame(self):
        success, frame = self.camera.read()
        if not success:
            return None
        else:
            frame = cv2.resize(frame, (160, 120))
            _, buffer = cv2.imencode('.jpg', frame)
            buffer = np.array(buffer)
            frame = buffer.tobytes()
            self.framenum += 1

        return frame

    def frameNbr(self):
        return self.framenum

    def fps(self):
        return self.FPS


class AUDIO:
    def __init__(self, filename):
        self.wf = wave.open(filename)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            frames_per_buffer=1024,
            input=True
        )
        self.FPS = self.wf.getframerate() / 1024
        self.framenum = 0

    def nextFrame(self):
        
        data = self.wf.readframes(1024)
        self.framenum += 1
        return data

    def frameNbr(self):
        return self.framenum

    def fps(self):
        return self.FPS

class MICRO:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=8,
            channels=1,
            rate=8000,
            frames_per_buffer=1024,
            input=True
        )
        self.FPS = 8000 / 1024
        self.framenum = 0

    def nextFrame(self):
        data = self.stream.read(1024)
        self.framenum += 1
        return data

    def frameNbr(self):
        return self.framenum

    def fps(self):
        return self.FPS