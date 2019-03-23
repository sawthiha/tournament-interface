import winsound as sound
import win32com.client as wincl
SAPI = wincl.Dispatch("SAPI.SpVoice")

import sys
sys.path.append('../')

import config.audio_config as config

def decor_sound(url):
	def wrapper():
		audio_file = url()
		sound.PlaySound(audio_file, sound.SND_FILENAME)

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
	SAPI.Speak("Hello World")