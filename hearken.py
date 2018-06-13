import ConfigParser, os, importlib
import sys
import signal

from common import snowboydecoder

#################################
# Check for interrupt signal
#################################

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


#################################
# Load from conf file
#################################

DEFAULT_MODULE = 'basic_ding'
CONF_FILE_NAME = 'hearken.conf'
ENV = 'demo'

# Count of hotwords said in short amount of time before firing action
HOTWORD_COUNT_THRESHHOLD = 2

# Selected module
SELECTED_MODULE = DEFAULT_MODULE

config = ConfigParser.SafeConfigParser()

# TODO: Allow for overwrite of conf file to use, with argparser

# Create .conf file with defaults if it doesn't exist
if not os.path.exists(CONF_FILE_NAME):
	print ".conf file does not exist. generating default conf"
	config.add_section('APP_RUNTIME')
	config.set('APP_RUNTIME', 'SELECTED_MODULE', SELECTED_MODULE)
	config.set('APP_RUNTIME', 'HOTWORD_COUNT_THRESHHOLD', '2')
	config.set('APP_RUNTIME', 'ENV', ENV)
	config.write(open(CONF_FILE_NAME, 'w'))

# Read existing conf and load the module
else:
	config.read(CONF_FILE_NAME)
	HOTWORD_COUNT_THRESHHOLD = config.getint('APP_RUNTIME', 'HOTWORD_COUNT_THRESHHOLD')
	SELECTED_MODULE = config.get('APP_RUNTIME', 'SELECTED_MODULE')
	ENV = config.get('APP_RUNTIME', 'ENV')

mod_import = 'modules.' + SELECTED_MODULE + '.' + SELECTED_MODULE

# Try to import module specified by conf file
# Quit with err msg if unsuccessful import
try: 
	mod = importlib.import_module(mod_import)
except ImportError:
	print "MODULE: " + SELECTED_MODULE + " does not exist. Please specify valid module."
	quit()

print "HOTWORD_COUNT_THRESHHOLD: ", HOTWORD_COUNT_THRESHHOLD
print "LOADED MODULE: " + SELECTED_MODULE
print "ENVIRONMENT: " + ENV

#################################
# Load module models and 
# action callbacks
#################################

module_load = mod.load_module(ENV)
models = module_load[0]
callbacks = module_load[1]

# TODO: Allow for sensitivity setting
sensitivity = [0.5]*len(models)

# Arm the hotword detector
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)


#################################
# Start listening
#################################


print 'Listening... Press Ctrl+C to exit'

# TODO: utilize the hotword count threshhold
# TODO: sleep_time into environment variable

# main loop
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()