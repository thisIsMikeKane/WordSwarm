# -*- coding: utf-8 -*-
""" Scraper_MIT_TECH_REVIEW.py

	This program is run first, before any of the other
	WordSarm programs, to scrape the MIT Tech Review
	Energy news feed and save the retrieved articles 
	to a binary (pickle) file to be read by Processor.py

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
from dateutil.parser import * # For parsing timestamps

# Classes
class Article:
    text = ''; # The entire text of the article to process
    date = ''; # Formatted as a string in UTC date format
articles = [];
    
# Base URL for MIT Technology Review - Energy Archive
baseURL = 'http://www.technologyreview.com/energy/stream/page/';

# Process HTML from each page
for k in range(1,250+1):

	# Download HTML and read into Soup
    response = urllib2.urlopen(baseURL + '%s' % k);
    soup = BeautifulSoup(response);
    
    # Parse HTML
	#  All articles are in an 'article' HTML class under a 'ul'
	#  with a class of type 'stream'. Extract text from the header 'h1'
	#  and all paragraphs within the 'article' HTML class. A time-stamp
	#  for the articles can be extracted from the 'time' within the
	#  HTML 'article' class in a standard UTC format.
    articles_raw = \
            soup.find('ul',attrs={'class':'stream'}).find_all('article');
    for a in articles_raw:
        articles.append(Article());
        articles[-1].text = a.h1.text;
        ps = a.find_all('p');
        for p in ps:
            if p.get('class') is None:
                articles[-1].text = articles[-1].text + ' ' +  p.text;
        if '(Week Ending ' in articles[-1].text:
			# Ignore summary articles in which the header text
			# begins with 'Week Ending '
            articles.pop();
        else:
            if ~(a.time.get('datetime') is None):
                articles[-1].date = parse(a.time.get('datetime'));   
            
            print(articles[-1].date.__str__());
       
# Save array of articles to binary file for later nGrams processing   
filename = 'article_data.out';
output = open(filename, 'wb');
pickle.dump(articles, output, -1);
output.close();