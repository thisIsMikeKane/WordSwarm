# -*- coding: utf-8 -*-
"""

	The module contains a class for word objects. The object contains
	the string containing the word, the word's colour, its aspect
	ratio used for scaling, and bounding box size. There is also a
	method for drawing the word to a position on the screen.
	
	The only thing to change here is the padding around each
	word to add a little better visual clash protection. 

	
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

import sys

# Import the PyBox2D/PyGame framework
sys.path.append('./framework') 
from framework import * # The abstracted PyBox2D framework
import pygame # The PyGame 'sub-framework'
from pygame.locals import * # Some parts of the PyGame framework to import locally

# Import WordSwarm modules
from wsColorer import * # Module for generating word colours

try: # Try to import advanced freetype font module 
    import pygame.freetype as freetype
except ImportError:
    print ("No FreeType support compiled")
    sys.exit ()

class wsWordObj(freetype.Font):

	padding = 20; # The number of pixels around the text of the word
			# to give a little better visual clash protection
	#@TODO Create an option for this that can be import from a 
	#	settings file and to scale with screen size.
			
	

	def __init__(self, string, hues):
		super(wsWordObj, self).__init__(None)
	
		self.colorer = wsColorer(hues) # Initialize the colourer
	
		self.string = string # Assign the string
		
		# Determine aspect ratio using a big size 
		#  to avoid rounding errors
		self.size = 100 
		self.fgcolor = list(self.colorer.getColor())
		self.render = self.render(self.string)[0]		
		
		# Calculate aspect ratio of textbox with padding
		self.boxSize = self.get_rect(self.string)[2:4] # Box size (px)
		self.paddedAR = (self.boxSize[1] + self.padding) / (float(self.boxSize[0]  + self.padding))
		self.paddedWScale = (self.boxSize[0] - self.padding) / float(self.boxSize[0])
		self.paddedHScale = (self.boxSize[1] - self.padding) / float(self.boxSize[1])
		
	def Draw(self, screen, pos):
	
		# Draw the word in a box of width of newSize(x,y) (px)	
		newSize = list((0,0))
		newSize[0] = int(self.boxSize[0] * self.paddedWScale)
		newSize[1] = int(self.boxSize[1] * self.paddedHScale) 
		scaledRender = pygame.transform.smoothscale(self.render, newSize)
		pos = list(pos)
		pos[0] = pos[0] - (newSize[0] / 2)
		pos[1] = pos[1] - (newSize[1] / 2)			
		screen.blit(scaledRender, pos)
