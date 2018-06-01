# Snowboy Hotword Detection - Multiple Models in a directory Demo

## Introduction

Expanding on the [snowboy](https://snowboy.kitt.ai/]) demo to provide an easy way to utilize multiple hotword detection models in a user specified directory

Groundwork project with plans to expand greater functionality - will eventually be integrated into slack or hue to get attention of open office coworkers who are wearing noise cancelling headphones

## Dependencies

To run the demo you will likely need the following, depending on which demo you
use and what platform you are working with:

* SoX (audio conversion)
* PortAudio or PyAudio (audio capturing)
* SWIG 3.0.10 or above (compiling Snowboy for different languages/platforms)
* ATLAS or OpenBLAS (matrix computation)

You can also find the exact commands you need to install the dependencies on
Mac OS X, Ubuntu or Raspberry Pi below.

### Mac OS X

`brew` install `swig`, `sox`, `portaudio` and its Python binding `pyaudio`:

    brew install swig portaudio sox
    pip install pyaudio

If you don't have Homebrew installed, please download it [here](http://brew.sh/). If you don't have `pip`, you can install it [here](https://pip.pypa.io/en/stable/installing/).

Make sure that you can record audio with your microphone:

    rec t.wav


### Ubuntu/Raspberry Pi/Pine64

First `apt-get` install `swig`, `sox`, `portaudio` and its Python binding `pyaudio`:

    sudo apt-get install swig3.0 python-pyaudio python3-pyaudio sox
    pip install pyaudio
    
Then install the `atlas` matrix computing library:

    sudo apt-get install libatlas-base-dev
    
Make sure that you can record audio with your microphone:

    rec t.wav
        
If you need extra setup on your audio (especially on a Raspberry Pi), please see the [full documentation](http://docs.kitt.ai/snowboy).


## Quick Start for Python Demo

Go to the `examples/Python` folder and open your python console:

    In [1]: import snowboydecoder
    
    In [2]: def detected_callback():
       ....:     print "hotword detected"
       ....:
    
    In [3]: detector = snowboydecoder.HotwordDetector("resources/snowboy.umdl", sensitivity=0.5, audio_gain=1)
    
    In [4]: detector.start(detected_callback)
    
Then speak "snowboy" to your microphone to see whether Snowboy detects you.

The `snowboy.umdl` file is a "universal" model that detect different people speaking "snowboy". If you want other hotwords, please go to [snowboy.kitt.ai](https://snowboy.kitt.ai) to record, train and downloand your own personal model (a `.pmdl` file).

When `sensitiviy` is higher, the hotword gets more easily triggered. But you might get more false alarms.

The file `multi-model-listener` can be called to test the baseline functionality 

You can execute the file with a directory of one or more hotwords and a ding will be heard everytime a hotword is detected


## Advanced Usages & Demos

See [Full Documentation](http://docs.kitt.ai/snowboy).

## Change Log

**v1.0.0**

* initial release
