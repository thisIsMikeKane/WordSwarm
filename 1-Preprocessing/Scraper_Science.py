# -*- coding: utf-8 -*-
""" Scraper_Science.py

	This program is run first, before any of the other
	WordSarm programs, to scrape the Science and save the 
	retrieved articles to a binary (pickle) 
	file to be read by Processor.py

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

# PubMed E-utils base URL
#   Explanation of PubMed E-utils:
#   http://www.ncbi.nlm.nih.gov/books/NBK25501/
base_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    
# Download list of articles from Science through PubMed
article_list = BeautifulSoup(urllib2.urlopen(base_url + 'esearch.fcgi?db=pubmed&term=Science%2E%5bJour%5d+NOT+%22Science%20(80-%20)%22+NOT+%22J%20Zhejiang%20Univ%20Sci%22&retmax=200000&retmode=xml'),"xml").IdList.findAll('Id')
print('Downloaded XML')

# Process XML from each
k = 0
N = 250 # Number of articles to retrieve at a time
articles = [None] * (len(article_list) -1)
for k in range(0, len(article_list), N):

	article_ID_short_list = article_list[k].text
	for k1 in range(k+1, min(k+N, len(article_list)-1)):
		article_ID_short_list += ',' + article_list[k1].text
		
	article_short_list_xml = BeautifulSoup(urllib2.urlopen(base_url + 'efetch.fcgi?db=pubmed&retmode=xml&id=' + article_ID_short_list),"xml").findAll('PubmedArticle')
	
	try:
		k1 = 0
		for article_xml in article_short_list_xml:
			
			articles[k+k1] = Article()
			articles[k+k1].text = article_xml.ArticleTitle.text
			for abstractText in article_xml.findAll('AbstractText'):
				articles[k+k1].text += abstractText.text
			
			dateStr = ''
			dateStr += article_xml.PubDate.Year.text
			try:
				dateStr += ' ' + article_xml.PubDate.Month.text
			except AttributeError:
				print('\tNo Month Found - Using Jan')
				dateStr += ' Jan'
				
			try:
				dateStr += ' ' + article_xml.PubDate.Day.text
			except AttributeError:
				print('\tNo Day Found - Using ''1''')
				dateStr += ' 1'
			
			articles[k+k1].date = parse(dateStr)
			
			k1 += 1
	except AttributeError:
		print('ERR: Bad XML entry')
		print(article_xml)
		print('/ERR: Bad XML entry')
		del articles[k+k1]
	
	print('Processed %d articles out %d'%(k, len(article_list)))
       
# Save array of articles to binary file for later nGrams processing   
filename = 'article_data.out';
output = open(filename, 'wb');
pickle.dump(articles, output, -1);
output.close();