# WordSwarm 
<img align="right" width="150px" src="https://github.com/thisIsMikeKane/WordSwarm/raw/master/wordSwarm_dark.png" />
Create an animated word cloud that helps visualize the variation
of word frequency in a time-series of 'articles'.
[Check out some example WordSwarms on YouTube](https://www.youtube.com/playlist?list=PLW9BhSPL6nfRFieaT0mqaAiZhA1ZFRzWX)

## Directory Structure

### `./1-Preprocessing/`
Programs in here are used from scraping data sources , calculating word frequency, and outputting a CSV file for further use.

- **`Scraper_\*.py`** Article source specific file for scraping the data and creating a binary file of the article text and dates for use by `Processor.py`.

- **`Processor.py`** Reads a binary file of article text and dates and outputs a CSV file of word frequency or count in each date bin. Expects a file in the current directory named `article_date.out` in the binary format proved by the example scraper.

- **`WordBlaclist.py`** A list of common words not to include in the output CSV file.

- **`text2ngram.exe`** The windows command line executable used to calculate the nGrams for a block of texts (i.e. all article text within a certain date range) 

### `./2-WordSwarm/`
Contains the program which actually generates the animated WordSwarm

- **`wordSwarm.py`** This is the actual program used to display the wordSwarm animation. Run `python wordSwarm -h` for usage instructions.
	
- **`/framework/`** This contains all of the framework files borrowed from PyBox2D and PyGame. Not much should need to be changed here. (The screen resolution can be changed here if need, but beware of scaling issues)

### `./3-PostProcessing/`
The programs in here are used to convert the frames saved by WordSwarm using the 'output frame' argument into a video file. 

- **`frames2video.bat`** Converts the individual frames created by `wordSwarm.py` into an H.264 video file. Assumes the default save argument `wordSwarm.py -s` was used. Uses the executable Windows binary of the open source program ffmpeg included, but also available from http://www.ffmpeg.org/ 


## Dependencies
Currently only tested and developed for Windows. The Beautiful Soup, Pyglet, PyGame, and PyBox2D modules can be installed using the WinPython Control Panel following [these instructions](https://code.google.com/p/winpython/wiki/ControlPanel)

* Python - Tested with [WinPython 32-bit `v2.7.6.4`](https://sourceforge.net/projects/winpython/files/WinPython_2.7/2.7.6.4/)
* Beautiful Soup - For parsing HTML. Tested with [`v4.3.2`](http://www.crummy.com/software/BeautifulSoup/#Download)
* Pyglet - Windowing and multimedia library. Tested with [`v1.1.4`](https://code.google.com/archive/p/pyglet/downloads). (May not actually be required)
* PyGame - For creating the animations. Tested with [`pygame-1.9.2a0.win32-py2.7.exe`](https://github.com/asweigart/inventwithpythondotcom/tree/master/static) 
* PyBox2D - Used for physics and clash detection of words in swarm. Tested with `Box2D-2.3b0.win32-py2.7.exe` available from https://code.google.com/p/pybox2d/downloads/list

## Usage
The following example describes how to create a WordSwarm using the AAAS Science Magazine as an example corpus

1. Install WinPython and all the dependencies listed above
2. Open an instance of `WinPython Command Prompt.exe`
	a. Change the directory `> cd <WordSwarm Directory>/1-Preprocessing/`
3. Run a scraper to parse source data into a format for later nGram calculations with the following command: `> python Scraper_Science.py`. 
	A. This will create a binary (pickle) file of all the articles and timestamps: `1-Preprocessing\article_data.out`
4. Run the processor `> python Processor.py` which will take the previously created binary file, copy text into bins for each date range, run the nGram calculation in each date range, then return a CSV file to `2-WordSwarm\nGramOut<Date_Ttime>.csv`. You can modify the beginning of `Processor.py` with the following options:
	- `win = 90` This sets the width of each date-range to 90 days
	- `lap = 30` This sets each date-range to increment by 30 days
	- `topN = 500` The final CSV file will have the top 500 results
	- `minFreq = 2` A word must show up at least twice in a date-range in order to be counted as a frequent word
	- `absCount = False` Means that word frequency is calculated relative to the number of words in each date-range as opposed to the total number of counts.
5. Change the directory `> cd <WordSwarm Directory>/2-WordSwarm/`
6. Run WordSwarm `> python wordSwarm.py -i nGramOut00000000000000.csv -s -m 15 -t "My First WordSwarm!"` in which the arguments mean:
	- `-i nGramOut00000000000000.csv` specifies which CSV file to create the WordSwarm for.
	- `-s` specifies that you want each frame to be saved as a PNG file for later processing into a movie
	- `-m 10` is a relative term that determines how large the largest word displayed on the screen will be.
	- `-t "My First WordSwarm` is the title that will be displayed in the top left corner of the WordSwarm
	- See `wordSwarm.py` for more commands to change word color, start date, and end date.
7. Change the directory `> cd <WordSwarm Directory>/3-Postprocessing/`
8. Convert the frames into a movie. `frames2video.bat`
	- This will create an output video file `wordSwarmOut.mp4`
	
Congratulations on creating your first WordSwarm!
