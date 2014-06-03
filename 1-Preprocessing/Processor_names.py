# -*- coding: utf-8 -*-
""" Processor_names.py

	This program is run first, before any of the other
	WordSarm programs, to scrape the US SSA name database
	and save the retrieved title and abstracts 
	to a binary (pickle) file to be read by Processor.py
	
	Date source: http://www.ssa.gov/oact/babynames/limits.html
	
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

import os # For file and directory handling
from dateutil.parser import * # For parsing timestamps
import csv # For reading the CSV file

# Options
topN = 500; # Number of most frequent words to use in final table

# Data location
dataPath = './names'
namesF = dict()
namesM = dict()
yearFCt = [0]*134
yearMCt = [0]*134

# Traverse all .txt file in dataPath
for dirname, dirnames, filenames in os.walk(dataPath):
	for filename in filenames:
		if filename[-4:] == '.txt':
		
			print(dirname, filename)
			year = int(filename[3:7])
			
			# Open CSV file from that year
			with open(os.getcwd() + dirname + '/' + filename, 'r') as csvfile:
				names = csv.reader(csvfile, delimiter=',')
				for row in names:
					if row[1] == 'F':
						if row[0] not in namesF:
							namesF[row[0]] = []
							namesF[row[0]].append([0,0])
							
						namesF[row[0]][0][1] += float(row[2])
						namesF[row[0]].append([year, float(row[2])])
						yearFCt[year-1880] += float(row[2])
						
					elif row[1] == 'M':
						if row[0] not in namesM:
							namesM[row[0]] = []
							namesM[row[0]].append([0,0])
							
						namesM[row[0]][0][1] += float(row[2])
						namesM[row[0]].append([year, float(row[2])])
						yearMCt[year-1880] += float(row[2])
						
# Calculate relative popularity
for name in namesF:
	for k in range(1, len(namesF[name])):
		namesF[name][k][1] = namesF[name][k][1] / yearFCt[namesF[name][k][0]-1880]
for name in namesM:
	for k in range(1, len(namesM[name])):
		namesM[name][k][1] = namesM[name][k][1] / yearMCt[namesM[name][k][0]-1880]
		
# Create and open output file csv with ordered name popularity table
f = open('../2-WordSwarm/names.csv','w')	

# Write first line of years
f.write('h') # Tell WordSwarm that hues are supplied
for yr in range(1880, 2014):
	f.write(',1/1/%d'%(yr))

# Output topN words
for n in range(0, topN):
	maxCount = 0
	for name in namesF:
		if namesF[name][0][1] > maxCount:
			topName = name
			topType = 'F'
			maxCount = namesF[name][0][1]
	for name in namesM:
		if namesM[name][0][1] > maxCount:
			topName = name
			topType = 'M'
			maxCount = namesM[name][0][1]
			
	# Write each name as the first column in the row
	print(topName)
	
	# Write the popularity for each year
	if topType == 'F':
		f.write('\nD4' + topName)
	
		for yr in range(1880, 2014):
			isWordUsed = False
			for k in range(1, len(namesF[topName])):
				if yr == namesF[topName][k][0]:
					f.write(',%f'%namesF[topName][k][1])
					isWordUsed = True
			if isWordUsed == False:
				f.write(',0')
		
		namesF.pop(topName, None)
			
	elif topType == 'M':
		f.write('\nAA' + topName)
	
		for yr in range(1880, 2014):
			isWordUsed = False
			for k in range(1, len(namesM[topName])):
				if yr == namesM[topName][k][0]:
					f.write(',%f'%namesM[topName][k][1])
					isWordUsed = True
			if isWordUsed == False:
				f.write(',0')
		
		namesM.pop(topName, None)
					
					
# Close output CSV file
f.close();