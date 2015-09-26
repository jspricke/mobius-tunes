#!/usr/bin/env python3

import signal
import sys
import wave
import re
import audioop
import random
import tempfile
import file_manager
import numpy as np
import numpy.fft as npf
import copy
from pydub import AudioSegment
from pydub.playback import play
from operator import itemgetter
import matplotlib.pyplot as plt
import rawCompare


yes = set(['yes','y', 'ye'])
no = set(['no','n'])

class mobius_py:

	def signal_handler(self, signal=signal.SIGINT, frame=None):
		choice = input('Would you like to keep your tmp files [yN]: ').lower()
		if choice in yes:
			print("Find your tmp files at: " + self.fileloader.get_tempfile())
		elif choice in no:
			self.fileloader.delete_tempfile()
		else:
			self.fileloader.delete_tempfile()

		sys.exit(0)

	def __init__(self, parts=500):
		self.fileloader = file_manager.file_manager()
		self.rawCompare = rawCompare.rawCompare()
		self.parts = parts
		signal.signal(signal.SIGINT, self.signal_handler)


	# returns a list of lists of points in the song with similar frequencies
	def loadConnections(self, playList):
		return []

	def fractureSong(self, song, connections):
		fragments = []
		i = 0
		while (i < len(connections)):
			i += 1
			fragments.append(song[:connections[i][0]])
			song = song[connections[i]:]
		return fragments

	def main(self):
		# get songs
		song = self.fileloader.load_from_mp3("testmusic/funkychunk.mp3", useTemp = False) #for each song

		self.fileloader.generate_tempfile()
		print(self.fileloader.get_tempfile())

		# Write mp3 to wav
		filename = self.fileloader.write_to_wav("filename.wav", song)

		# Get only last bit of filename. If this errors, no match!
		match = re.compile("[^/\\\\]*$").search(filename.name).group()


		wavedata, rawdata = self.fileloader.get_raw_from_wav(match)

		# PERFORM SOME CHANGES
		#
		# Test modification

		#print (self.rawCompare.compare(copy.deepcopy(rawdata), 500))

		playList = []
		playList.append(song)

		# load connections list with song links
		connections = self.loadConnections(playList)
		sorted(connections, key = itemgetter(0))

		# Write changes
		self.fileloader.write_raw_to_wav("temporaryOutput.wav", wavedata, rawdata)
		song = self.fileloader.load_from_wav("temporaryOutput.wav")

		self.fileloader.play_raw_data(wavedata, rawdata)

		# play song. We need to allow the song to randomly jump via connections[]
		songFragments = self.fractureSong(song, connections)
		# play(song)

		# Do not remove unless debugging
		self.signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
	mobius = mobius_py()
	mobius.main()