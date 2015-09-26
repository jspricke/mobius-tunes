import wave
import shutil
import copy
import audioop
import random
import os
import tempfile
import file_manager
import pyaudio
from pydub import AudioSegment
from pydub.playback import play
from operator import itemgetter
import time

#define stream chunk
chunk = 1024

class file_manager(object):

	def __init__(self):
		self.temporaryfile = None

	def generate_tempfile(self):
		self.temporaryfile = tempfile.mkdtemp()
		self.temporaryfile = self.temporaryfile + "/"
		return copy.deepcopy(self.temporaryfile)

	def get_tempfile(self):
		return copy.deepcopy(self.temporaryfile)

	def delete_tempfile(self, path = None):
		if path == None:
			path = self.temporaryfile
		if path == None:
			print("Temp File was not created yet!")
			return
		shutil.rmtree(path)

	def set_tempfile(self, path):
		if path[-1:] != "/":
			path = path + "/"
		self.temporaryfile = path

	def __sanitize__(self, useTemp = True):
		if (useTemp == False) :
			return ""
		if self.temporaryfile == None:
			self.generate_tempfile()
		return self.temporaryfile


	def load_from_mp3(self, path, useTemp = True):
		prefix = self.__sanitize__(useTemp)
		return AudioSegment.from_mp3(prefix + path)

	def write_to_wav(self, path, toWrite, useTemp = True): #
		prefix = self.__sanitize__(useTemp)
		return toWrite.export(prefix + path, format="wav")

	def get_raw_from_wav(self, path, useTemp = True):
		prefix = self.__sanitize__(useTemp)
		toopen = wave.open(prefix +  path)
		toopen.setpos(0)

		return toopen.getparams(), toopen.readframes(toopen.getnframes())

	def load_from_wav(self, path, useTemp = True):
		prefix = self.__sanitize__(useTemp)
		return AudioSegment.from_wav(prefix +  path)

	def write_raw_to_wav(self, path, waveparams, rawdata, useTemp = True):
		prefix = self.__sanitize__(useTemp)
		tempWrite = wave.open(prefix +  path, mode = 'wb')
		tempWrite.setnchannels(waveparams[0])
		tempWrite.setsampwidth(waveparams[1])
		tempWrite.setframerate(waveparams[2])
		tempWrite.setnframes(waveparams[3])
		tempWrite.writeframesraw(rawdata)

	def play_raw_data(self, waveparams, rawdata):
		#open a wav format music
		f = wave.open(r"/usr/share/sounds/alsa/Rear_Center.wav","rb")
		#instantiate PyAudio
		p = pyaudio.PyAudio()
		#open stream
		stream = p.open(format = p.get_format_from_width(waveparams[1]),
						channels = waveparams[0],
						rate = waveparams[2],
						output = True)
		#read data
		counter = 0

		#paly stream
		while counter + chunk < len(rawdata):
			stream.write(rawdata[counter:counter + chunk])
			counter = counter + chunk
			time.sleep((chunk/waveparams[2])/1000)

		#stop stream
		stream.stop_stream()
		stream.close()

		#close PyAudio
		p.terminate()