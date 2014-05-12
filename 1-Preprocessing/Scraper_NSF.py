# -*- coding: utf-8 -*-
""" Scraper_NSF.py

	This program is run first, before any of the other
	WordSarm programs, to scrape the NSF award archive
	and save the retrieved title and abstracts 
	to a binary (pickle) file to be read by Processor.py
	
	Download and extract all of the archives from the NSF
	website (http://www.nsf.gov/awardsearch/download.jsp).
	You should have a folder for each year, each containing
	XML files for each award. FYI, this is 2.11GB of data.
	
	Make sure to change the dataPath variable to match
	your computer's directory structure.
	

	This file is part of WordSwarm.

    WordSwarm is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    WordSwarm is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

	Copyright 2014 Michael Kane

	@author: Michael Kane
"""

# Import modules
import urllib2; # For downloading HTML pages
from bs4 import BeautifulSoup # For parsing HTML pages
import pickle; # For saving data to binary file for later nGram processing
import os # For file and directory handling
from dateutil.parser import * # For parsing timestamps

# Classes
class Article:
    text = ''; # The entire text of the article to process
    date = ''; # Formatted as a string in UTC date format
articles = [];
    
# Data location
dataPath = './NSF';

# Traverse all xml files in subdirectories of the dataPath
for dirname, dirnames, filenames in os.walk(dataPath):
	for filename in filenames:
		if filename[-4:] == '.xml':
			print(dirname, filename)
			
			data = open(os.getcwd() + dirname + '/' + filename, 'r')
			soup = BeautifulSoup(data)
			
			articles.append(Article());
			articles[-1].text = soup.find('awardtitle').text + soup.find('abstractnarration').text
			articles[-1].date = parse(soup.find('awardeffectivedate').text)
			
# Save array of articles to binary file for later nGrams processing   
filename = 'article_data.out'
output = open(filename, 'wb')
pickle.dump(articles, output, -1)
output.close()
			