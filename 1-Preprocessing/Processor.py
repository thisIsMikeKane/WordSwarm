# -*- coding: utf-8 -*-
""" NGramProcessor.py

	The program is run second, after the scraper and before
	other WordSarm programs. It reads in the binary (pickle)
	file created by the scrapper, and processes by binnning 
	the articles by dates, then calculates the nGrams for each
	bin. The top nGram results are then formatted into a CSV
	file to be read by the actual WordWarm.py program

	Original list of words retrieved from 
	open source software WordCarm from here:
	https://wordcram.googlecode.com/svn/javadoc/constant-values.html
	

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
import os; # For OS directory/file handling
import pickle; # For reading binary file created by scraper
import datetime # For processing dates
import re # Regular expressions for removing black listed words
from WordBlacklist import WordBlacklist # A blacklist of words
	# not to include in nGram calculations
import subprocess # For running text2ngram executable
import string # For parsing output string of text2ngram
import operator # For sorting class arrays

# Options
win = 90; # Days to average articles over
lap = 30; # Overlap in windows 
topN = 500; # Number of most frequent words to use in final table
minFreq = 2; # Minimum frequency with which a word must show up to be counted
absCount = False # Generate ngrams based on absolute count or relative frequency

# Debugging/advanced options
scraperOutFN = 'article_data.out'
createBinFiles = True # Set to false for debugging

# Classes
class Article:
	text = '';
	date = ''; 

class nGram:
	word = '';
	count = '';
nGrams = [] # 2-D array of calculated nGrams 
	# [Date Window][Order in which words were found in window]
	#@todo This is not very memory efficient since the word
	#	string is repeated for each date-window

# Import scraped date
print('Importing article array from: %s' % scraperOutFN)
pkl_file = open(scraperOutFN, 'rb');
articles = pickle.load(pkl_file);
pkl_file.close();
print('Successfully imported %d articles' % len(articles))
articles = articles[0:-1]

# Remove blacklisted words from articles
remove = '|'.join(WordBlacklist);
regex = re.compile(r'\b('+remove+r')\b', flags=re.IGNORECASE)

# Make upper-case and remove non-alphanumeric 
#  (except apostrophes for contractions)
if createBinFiles: 
	print('Cleaning blacklist of words from articles')
	for aN in range(0,len(articles)):
		if (aN % 1000) == 0:
			print('Cleaned upto %s' % articles[aN].date.__str__())
		articles[aN].text = re.sub(r'[^\w\']', ' ', articles[aN].text.upper());
		articles[aN].text = regex.sub("", articles[aN].text);	
	print('Done cleaning articles')

# Organize articles by date
articles = sorted(articles, key=operator.attrgetter('date')); # Sort list by oldest first
dateS = articles[0].date; # First article date
# dateS = datetime.datetime.strptime('19500101','%Y%m%d'); # Use a different starting date#
dateE = articles[-1].date; # Last article date

# Create output directory if required
if not os.path.exists('./nGramInput/'):
	os.makedirs('./nGramInput/')
else:
	# Removes files from a directory matching a pattern
	for f in os.listdir('./nGramInput/'):
		if re.search('.*', f):
			os.remove(os.path.join('./nGramInput/', f))	

# Prep for separating articles into date-based bins
dateSk = dateS; # Start date in current date-window
dateEk = dateS + datetime.timedelta(win); # End date in current date-window
fName = []; # List of file names for each date-window
fSize = []; # Number of words found in all articles within date-window
fDate = (dateSk + datetime.timedelta(win/2))
fName.append('./nGramInput/%04d%02d%02d.txt'%(fDate.year,fDate.month,fDate.day))
fSize.append(0)
print(fName[-1]);
if createBinFiles: f = open(fName[-1],'w');

# Put all the articles into date-based bins 
print('Creating article bins')
for aN1 in range(0,len(articles)):
	# Loop through articles to find first 
	#  article to put into a bin. This requires
	#  parsing the date in string UTC format
	#  into a native binary format.
	if articles[aN1].date >= dateSk:
	
		# Write current articles text to bin file
		#  and count number of words added
		if createBinFiles: f.write(articles[aN1].text + '\n');
		fSize[-1] = fSize[-1] + len(articles[aN1].text.split())
		
		for aN2 in range(aN1+1,len(articles)):		
		
			# Find rest of articles within current window
			if ((articles[aN2].date <= dateEk)
					and (aN2 <> len(articles) - 1)):
					
				# Write current articles text to bin file
				#  and count number of words added					
				if createBinFiles: f.write(articles[aN2].text + '\n');
				fSize[-1] = fSize[-1] + len(articles[aN2].text.split())
				
			# If the last article has been passed then
			#  close window file and go to next window
			else:
				
				if createBinFiles: f.close();
				dateSk += datetime.timedelta(lap);
				dateEk += datetime.timedelta(lap);
				fDate = (dateSk + datetime.timedelta(win/2))
				fName.append('./nGramInput/%04d%02d%02d.txt'%(
						fDate.year,fDate.month,fDate.day))
				fSize.append(0)
				print(fName[-1]);
				if createBinFiles: f = open(fName[-1],'w');
				break
				
articles = None; # Free memory
if createBinFiles: f.close(); # Close last file
			
# Prepare nGram table
dic = {}; # The unsorted dictionary of words found in all nGram runs
	# where the definition is the array of counts followed by countSum
			
# Run nGram on each date-window
p = None
nResults = 0
for fN in range(0,len(fName)):
	print(fName[fN])
	
	# Run the external nGram calculator process, then
	#  extract output from text2ngram that was returned.
	#
	#  The text2ngram.exe executable is an open source
	#  project that can be retreived from:
	#  http://homepages.inf.ed.ac.uk/lzhang10/ngram.html
	# 
	#  Options specify find words that show up more than twice (-f2)
	#  that are between one word (-n1) and two words (-n2) long
	if not p is None: # Clean up previous sub-processes
		p.stdout.close()
		p.stderr.close()
		p.terminate()
		p.kill()
		p = None
		
	p = subprocess.Popen(["text2ngram", "-n1", "-m1", "-f%d"%minFreq, \
			fName[fN]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err = p.communicate()
	out = out.split('\r\n');

	# Each line (after the first three) of the text2ngram output 
	#  contains the string followed by the number of occurrences
	for k in range(3,len(out)):
		if not out[k] == '':
			
			# Remove unprintable characters
			out[k] = ''.join(filter(lambda x: x in string.printable, out[k]));
			
			# Extract word and count
			word = re.sub(r' [0-9]*$', '', out[k]);
			count = float(re.findall(r'[0-9]*$',out[k])[0]);
			
			# If word was found add it to output
			if len(word) > 1:
				try:
					
					dic[word][fN] = count
					dic[word][-1] = dic[word][-1] + count
					nResults = nResults + 1
					
				except KeyError:
				
					cntAndSum = [0]*(len(fName) + 1)
					cntAndSum[fN] = count
					cntAndSum[-1] = cntAndSum[-1] + count
					dic[word] = cntAndSum
					nResults = nResults + 1
					print('Dictionary has %d words out of %d results' % (len(dic), nResults))
		
if not absCount:
	# Convert nGram table from absolute count to 
	#  frequency within each date-window
	for word in dic:
		dicNCounts = dic[word]
		dicNCounts[-1] = dicNCounts[-1] / len(fName)
		for winN in range(0, len(fName)):
			if fSize[winN] <> 0:
				dicNCounts[winN] = dicNCounts[winN] / float(fSize[winN])
		dic[word] = dicNCounts

						
# Create and open output file csv with nGram table
f = open('../2-WordSwarm/nGramOut' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv','w');

# Write the date row to file
for winN in range(0,len(fName)):
	f.write(',%s/%s/%s' % (fName[winN][13:21][4:6], fName[winN][13:21][6:8], fName[winN][13:21][0:4]));

# Find total count of most common word
for topWordN in range(0, topN):
	maxCount = 0
	for word in dic:
		if dic[word][-1] > maxCount:
			topWord = word
			maxCount = dic[word][-1]
	
	# Write each word as the first column in the row
	print(topWord)
	f.write('\n' + topWord + ',');
	
	# Write the counts (or frequency) found within each window
	dicNCounts = dic[topWord]
	for winN in range(0,len(fName)):
		f.write(repr(dicNCounts[winN]) + ',');			
	
	# Remove top word from diction to find next top
	del dic[topWord]			

# Close output CSV file
f.close();