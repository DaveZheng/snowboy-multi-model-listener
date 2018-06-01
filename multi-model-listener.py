import os, os.path 

import snowboydecoder
import sys
import signal

# Code for loading all hotwords in a directory to use for hotword detection
# Able to handle multiple models; however performance degrades if model count is sufficiently large

# args: sys.argv[1] should have the hotword directory, containing valid .umdl and .pmdl files

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


# Handle passed in arguments

# Exit on no args passed
if len(sys.argv) < 2:
    print "Error: need to specify directory in workspace that contains at least two files!"
    print "Usage: python hotwords-dir/"
    sys.exit(-1)

else:

    # Check to see whether directory is valid and has at least 1 hotword file; exit otherwise
    try:
        hotword_dir = os.path.join(os.getcwd(), sys.argv[1])

        print 'Attempting to load hotwords from directory: ', hotword_dir

        hotword_dir_files = os.listdir(hotword_dir)
        hotword_files = [f for f in hotword_dir_files if (f.endswith('.umdl') or f.endswith('.pmdl'))]

        if len(hotword_files) == 0:
            print("Error: need to specify directory in workspace that contains at least two files!")
            print("Usage: python ./hotwords-dir/")
            sys.exit(-1)
        else: 
            print "Loaded {0} hotword files: ".format(len(hotword_files))
            print hotword_files
        
    except OSError:
        print "No such directory: ", os.path.join(os.getcwd(), sys.argv[1])
        sys.exit(-1)
    except:
        print "Unexpected error:", sys.exc_info()[0]


models = [os.path.join(sys.argv[1], f) for f in hotword_files]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Set sensitivity to default recommended - adjust based on snowboy documentation
sensitivity = [0.5]*len(models)

detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)

# callbacks
callbacks = [lambda: snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING) for model in models]


print 'Listening... Press Ctrl+C to exit'

# main loop
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
