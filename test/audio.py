import sys
sys.path.append('../')

PLATFORM = sys.platform

if PLATFORM.startswith('win'):
	import winsound as sound
	import win32com.client as wincl
elif PLATFORM.startswith('linux'):
	import wave
	import pyaudio
	import os
elif PLATFORM.startswith('dar'):
	raise NotImplementedError()
else:
	raise NotImplementedError()

import config.audio_config as config

class Sound:
	def __init__(self, impl):
		self._impl = impl

	def play(self, url):
		self._impl.play(url)

	def tts(self, text):
		self._impl.tts(text)

	def setImpl(self, impl):
		self._impl = impl

	def getImpl(self):
		return self._impl

	def keypressed(self):
		url = config.KEY_PRESSED
		self._impl.play(url)

	def candidatechanged(self, no):
		self._impl.tts(str(no))

	def stepchanged(self):
		url = config.STEP
		self._impl.play(url)

class WinSoundImpl:
	def __init__(self):
		self.sapi = wincl.Dispatch("SAPI.SpVoice")

	def play(self, url):
		sound.PlaySound(url, sound.SND_FILENAME)

	def tts(self, text):
		self.sapi.Speak(text)

class LinSoundIml:
	def play(self, url):
		raw_audio = wave.open(url, mode = 'rb')
		device = pyaudio.PyAudio()
		n_channels, sample_width, frame_rate, n_frames, t_comp, name_comp = raw_audio.getparams()
		
		def callback(in_data, n_frames, time, status):
			data = raw_audio.readframes(n_frames)
			return data, pyaudio.paContinue
		
		stream = device.open(
				format = device.get_format_from_width(sample_width),
				channels = n_channels,
				rate = frame_rate,
				output = True
			)
		data = raw_audio.readframes(n_frames)
		stream.write(data)
		stream.stop_stream()
		device.terminate()
		raw_audio.close()
		stream.close()

	def tts(self, text):
		cmd = 'espeak ' + '\'' + text + '\''
		os.system(cmd)

class OSXSoundImpl:
	def play(self, url):
		raise NotImplementedError()

	def tts(self, text):
		raise NotImplementedError()

def sound():
	if PLATFORM.startswith('win'):
		impl = WinSoundImpl()
	elif PLATFORM.startswith('linux'):
		impl = LinSoundIml()
	else:
		impl = OSXSoundImpl()
	return Sound(impl)

AUDIO = sound()
AUDIO.play('../resource/sound/lo-fi.wav')