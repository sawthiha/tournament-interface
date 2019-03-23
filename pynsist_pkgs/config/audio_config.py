import config.config as config

audio = config.config['AUDIO']
KEY_PRESSED = config.from_root(audio['key'])
CANDIDATE = config.from_root(audio['candidate'])
STEP = config.from_root(audio['step'])