##WordSwarm
Create an animated word cloud that helps visualize the variation
of word frequency in a time-series of 'articles'.


#Directory Structure

**`./1-Preprocessing/`**
Programs in here are used from scraping data sources , calculating word frequency, and outputting a CSV file for further use.

	- **`Scraper_\*.py`** Article source specific file for scraping the data and creating a binary file of the article text and dates for use by `Processor.py`.

	- **`Processor.py`** Reads a binary file of article text and dates and outputs a CSV file of word frequency or count in each date bin. Expects a file in the current directory named `article_date.out` in the binary format proved by the example scraper.

	- **`WordBlaclist.py`** A list of common words not to include in the output CSV file.

	- **`text2ngram.exe`** The windows command line executable used to calculate the nGrams for a block of texts (i.e. all article text within a certain date range) 

**`./2-WordSwarm/`**
Contains the program which actually generates the animated WordSwarm

	- **`wordSwarm.py`** This is the actual program used to display the wordSwarm animation. Run `python wordSwarm -h` for usage instructions.
	
	- **`/framework/`** This contains all of the framework files borrowed from PyBox2D and PyGame. Not much should need to be changed here. (The screen resolution can be changed here if need, but beware of scaling issues)

**`./3-PostProcessing/`**
The programs in here are used to convert the frames saved by WordSwarm using the 'output frame' argument into a video file. 

	- **`frames2video.bat`** Converts the individual frames created by `wordSwarm.py` into an H.264 video file. Assumes the default save argument `wordSwarm.py -s` was used. Uses the executable Windows binary of the open source program ffmpeg included, but also available from http://www.ffmpeg.org/ 


#Dependencies
Currently only tested and developed for Windows. The Beautiful Soup, Pyglet, PyGame, and PyBox2D modules can be installed using the WinPython Control Panel following [these instructions](https://code.google.com/p/winpython/wiki/ControlPanel)

* Python - Tested with [WinPython 32-bit `v2.7.6`](http://sourceforge.net/projects/winpython/files/WinPython&95;2.7/2.7.6.4)
* Beautiful Soup - For parsing HTML. Tested with [`v4.3.2`](http://www.crummy.com/software/BeautifulSoup/#Download)
* Pyglet - Windowing and multimedia library. Tested with [`v1.1.4`](http://pyglet.googlecode.com/files/pyglet-1.1.4.zip). (May not actually be required)
* PyGame - For creating the animations. Tested with `pygame-1.9.2a0.win32-py2.7.exe` available from [Christoph Gohlke site](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame) 
* PyBox2D - Used for physics and clash detection of words in swarm. Tested with `Box2D-2.3b0.win32-py2.7.exe` available from https://code.google.com/p/pybox2d/downloads/list

#Usage
The following example describes how to create the WordSwarm for the NSF award archive

1. 