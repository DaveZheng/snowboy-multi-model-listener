import os, os.path
import sys
import json
import pyaudio
import time
import wave

import pprint

from common import snowboydecoder

MODULE_PATH = os.path.dirname(__file__)
CONFIG_FILE_NAME = "config.json"

# Sound resource files

DETECT_DING = os.path.join(MODULE_PATH, "resources/ding.wav")
DETECT_DING = os.path.join(MODULE_PATH, "resources/dong.wav")

# TODO: extend an abstract class with load_models and loadCallbacks

# TODO: can be a parent class method to avoid repitition
def load_models(pEnv):

	try:
		env_dir = os.path.join(MODULE_PATH, pEnv)

		print 'Attempting to load models from module directory: ', env_dir

		env_dir_files = os.listdir(env_dir)
		model_files = [f for f in env_dir_files if (f.endswith('.umdl') or f.endswith('.pmdl'))]

		if len(model_files) == 0:
			print("Error: module and environment combination needs at least 1 associated model! (.umdl, .pmdl).")
			print("There are no model files in ", env_dir)
			sys.exit(-1)
		else: 
			print "Loading {0} hotword files: ".format(len(model_files))
			print model_files
			
	except OSError:
		print "No such directory: ", env_dir
		sys.exit(-1)
	except:
		print "Unexpected error:", sys.exc_info()[0]
	
	return [os.path.join(env_dir, f) for f in model_files]


# Loads the module
# params: pEnv string		name of environment
# returns	arr 					[model, callbacks], callback is the custom action for the module

# TODO: can be abstracted

def load_module(pEnv):

	models = load_models(pEnv)

	try:
		env_file = os.path.join(MODULE_PATH, pEnv, CONFIG_FILE_NAME)

		print 'Attempting to load config file from: ', env_file

		with open(env_file) as f:
			config = json.load(f)

			pp = pprint.PrettyPrinter(indent=4)
			pp.pprint(config)
			print config[0].name

			# TODO: add routing to different callback actions

			return [models, [lambda: module_action(DETECT_DING) for model in models]]

	except:
		print "Unexpected error:", sys.exc_info()[0]
		sys.exit(-1)	


def module_action(fname=DETECT_DING):
    """Simple callback function to play a wave file. By default it plays
    a Ding sound.

    :param str fname: wave file name
    :return: None
    """
    ding_wav = wave.open(fname, 'rb')
    ding_data = ding_wav.readframes(ding_wav.getnframes())
    audio = pyaudio.PyAudio()
    stream_out = audio.open(
        format=audio.get_format_from_width(ding_wav.getsampwidth()),
        channels=ding_wav.getnchannels(),
        rate=ding_wav.getframerate(), input=False, output=True)
    stream_out.start_stream()
    stream_out.write(ding_data)
    time.sleep(0.2)
    stream_out.stop_stream()
    stream_out.close()
    audio.terminate()


