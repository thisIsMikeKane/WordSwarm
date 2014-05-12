# -*- coding: utf-8 -*-
"""

	The module contains a class that is used to store all of the 
	nGrams and their time histories. This includes a list of words,
	a list of dates, and a matrix of the word counts (or frequencies)
	at each date. 

	Dates in CSV file should be in the form of MM/DD/YYYY
		
	
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
"""

import csv
import datetime

class wsNGrams:
	words = [] # List of words
	counts = [] # Matrix of word counts (or frequencies) 
		# [word index][Date index]
	dates = [] # List of dates
	nDates = 0 # Total number of dates
	nWords = 0 # Total number of words
	maxCount = 0 # Count of the word with the highest count
		# in any given date-bin
	
	def __init__(self,fName, startDateStr, endDateStr):
	
		if startDateStr is None:
			startdate = datetime.datetime.strptime('00010101','%Y%m%d');
		else:
			startdate = datetime.datetime.strptime(startDateStr,'%Y%m%d');
			
		if endDateStr is None:
			enddate = datetime.datetime.strptime('99991231','%Y%m%d');
		else:
			enddate = datetime.datetime.strptime(endDateStr,'%Y%m%d');
	
		# Import data from CSV file
		with open(fName, 'rb') as csvfile:
			fNgrams = csv.reader(csvfile) # Open CSV file
			rowN = 0
			for row in fNgrams: # Process each row in CSV file
			
				if rowN == 0: # Import dates
				
					startdateK = 0;
					for dateStr in row[1:]:
						if datetime.datetime.strptime(dateStr,'%m/%d/%Y') < startdate:
							startdateK = startdateK+1
						else:
							break;
							
					enddateK = 0;
					for	dateStr in row[1:]:
						if datetime.datetime.strptime(dateStr,'%m/%d/%Y') < enddate:
							enddateK = enddateK+1;
						else:
							break;
					enddateK = enddateK-1;
					
					for dateStr in row[startdateK+1:enddateK+2]:
						self.dates.append(datetime.datetime.strptime(dateStr,'%m/%d/%Y'))
						
					self.nDates = len(self.dates)
					
				elif rowN>0: # Import words and counts
				
					self.counts.append([0]*self.nDates)
					self.words.append(row[0])
					
					for countN in range(startdateK, enddateK+1):
						count = float(row[countN+1])
						self.counts[rowN-2][countN-startdateK] = count
						if count>self.maxCount:
							self.maxCount = count
					
				rowN = rowN+1
	
		self.nWords = len(self.words)