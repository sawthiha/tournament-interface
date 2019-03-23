import playsound as sound

import sys
sys.path.append('../')

import config.audio_config as config

class Sound:
	def __init__(self):
		raise NotImplementedError()

class WinSound:
	def __init__(self):
		raise NotImplementedError()

	def play():
		sound

def decor_sound(url):
	def wrapper():
		audio_file = url()
		sound.playsound(audio_file)
	return wrapper

@decor_sound
def keyPressed():
	return config.KEY_PRESSED

@decor_sound
def candidateChanged():
	return config.CANDIDATE

@decor_sound
def stepChanged():
	return config.STEP

def tts(text):
	raise NotImplementedError()

keyPressed()