import os, os.path
import sys

from common import snowboydecoder

MODULE_PATH = os.path.dirname(__file__)

# TODO: extend an abstract class with loadModels and loadCallbacks

# TODO: Setup and Run commands 

def loadModels(pEnv):

	try:
		env_dir = os.path.join(MODULE_PATH, pEnv)

		print 'Attempting to load models from directory: ', env_dir

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


def loadCallbacks(pModels):

	return [lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING) for model in pModels]