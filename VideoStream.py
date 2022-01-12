import cv2
import numpy as np
import moviepy.editor as mp
from scipy.io import wavfile

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
		data = self.file.read(5) # Get the framelength from the first 5 bits
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
		self.filename = filename
		try:
			sample_rate, self.audio = wavfile.read(filename)
			self.FPS = sample_rate // 4
		except:
			raise IOError
		self.framenum = 0

	def nextFrame(self):
		num = self.framenum
		buffer = self.audio[num: num + 2000]
		a_frame = buffer.tobytes()
		self.framenum += 2000
		return a_frame

	def frameNbr(self):
		return self.framenum

	def fps(self):
		return self.FPS
