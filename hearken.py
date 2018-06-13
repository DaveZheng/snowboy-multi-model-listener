import ConfigParser, os, importlib
# import modules.basic_ding.basic_ding

DEFAULT_MODULE = 'basic_ding'
CONF_FILE_NAME = 'hearken.conf'

SELECTED_MODULE = DEFAULT_MODULE

config = ConfigParser.SafeConfigParser()

# TODO: Allow for overwrite of conf file to use, with argparser

# Create .conf file if it doesn't exist
if not os.path.exists(CONF_FILE_NAME):
	print ".conf file does not exist. generating default conf"
	config.add_section('APP_RUNTIME')
	config.set('APP_RUNTIME', 'SELECTED_MODULE', SELECTED_MODULE)
	config.write(open(CONF_FILE_NAME, 'w'))

# Read existing conf and load the module
else:
	config.read(CONF_FILE_NAME)
	SELECTED_MODULE = config.get('APP_RUNTIME', 'SELECTED_MODULE')

mod_import = 'modules.' + SELECTED_MODULE + '.' + SELECTED_MODULE

# Try to import module specified by conf file
# Quit with err msg if unsuccessful import
try: 
	mod = importlib.import_module(mod_import)
except ImportError:
	print "MODULE: " + SELECTED_MODULE + " does not exist. Please specify valid module."
	quit()

print "LOADED MODULE: " + SELECTED_MODULE

# TODO: Run SETUP and LISTEN commands to start the app