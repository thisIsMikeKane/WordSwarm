# -*- coding: utf-8 -*-
"""

	

	
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
	
	PyBox2D Framework:

	This software is provided 'as-is', without any express or implied
	warranty.  In no event will the authors be held liable for any damages
	arising from the use of this software.
	Permission is granted to anyone to use this software for any purpose,
	including commercial applications, and to alter it and redistribute it
	freely, subject to the following restrictions:
	1. The origin of this software must not be misrepresented; you must not
	claim that you wrote the original software. If you use this software
	in a product, an acknowledgment in the product documentation would be
	appreciated but is not required.
	2. Altered source versions must be plainly marked as such, and must not be
	misrepresented as being the original software.
	3. This notice may not be removed or altered from any source distribution.	
	
	C++ version Copyright (c) 2006-2007 Erin Catto http://www.box2d.org
	Python version by Ken Lauer / sirkne at gmail dot com

"""

# Form implementation generated from reading ui file 'pyqt4_gui.ui'
#
# Created: Sun Mar 13 19:19:05 2011
#      by: PyQt4 UI code generator 4.7.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.mnuFile = QtGui.QMenu(self.menubar)
        self.mnuFile.setObjectName(_fromUtf8("mnuFile"))
        self.menu_Options = QtGui.QMenu(self.menubar)
        self.menu_Options.setObjectName(_fromUtf8("menu_Options"))
        self.menu_Font_size = QtGui.QMenu(self.menu_Options)
        self.menu_Font_size.setObjectName(_fromUtf8("menu_Font_size"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.dwProperties = QtGui.QDockWidget(MainWindow)
        self.dwProperties.setObjectName(_fromUtf8("dwProperties"))
        self.dwcProperties = QtGui.QWidget()
        self.dwcProperties.setObjectName(_fromUtf8("dwcProperties"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dwcProperties)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbOptions = QtGui.QGroupBox(self.dwcProperties)
        self.gbOptions.setObjectName(_fromUtf8("gbOptions"))
        self.verticalLayout.addWidget(self.gbOptions)
        self.twProperties = QtGui.QTableWidget(self.dwcProperties)
        self.twProperties.setLineWidth(1)
        self.twProperties.setAlternatingRowColors(True)
        self.twProperties.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.twProperties.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.twProperties.setObjectName(_fromUtf8("twProperties"))
        self.twProperties.setColumnCount(0)
        self.twProperties.setRowCount(0)
        self.verticalLayout.addWidget(self.twProperties)
        self.dwProperties.setWidget(self.dwcProperties)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dwProperties)
        self.mnuExit = QtGui.QAction(MainWindow)
        self.mnuExit.setObjectName(_fromUtf8("mnuExit"))
        self.mnuIncreaseFontSize = QtGui.QAction(MainWindow)
        self.mnuIncreaseFontSize.setObjectName(_fromUtf8("mnuIncreaseFontSize"))
        self.mnuDecreaseFontSize = QtGui.QAction(MainWindow)
        self.mnuDecreaseFontSize.setObjectName(_fromUtf8("mnuDecreaseFontSize"))
        self.mnuFile.addAction(self.mnuExit)
        self.menu_Font_size.addAction(self.mnuIncreaseFontSize)
        self.menu_Font_size.addAction(self.mnuDecreaseFontSize)
        self.menu_Options.addAction(self.menu_Font_size.menuAction())
        self.menubar.addAction(self.mnuFile.menuAction())
        self.menubar.addAction(self.menu_Options.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "pybox2d testbed", None, QtGui.QApplication.UnicodeUTF8))
        self.mnuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Options.setTitle(QtGui.QApplication.translate("MainWindow", "&Options", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Font_size.setTitle(QtGui.QApplication.translate("MainWindow", "&Font size", None, QtGui.QApplication.UnicodeUTF8))
        self.dwProperties.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.gbOptions.setTitle(QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.twProperties.setSortingEnabled(True)
        self.mnuExit.setText(QtGui.QApplication.translate("MainWindow", "E&xit", None, QtGui.QApplication.UnicodeUTF8))
        self.mnuIncreaseFontSize.setText(QtGui.QApplication.translate("MainWindow", "&Increase", None, QtGui.QApplication.UnicodeUTF8))
        self.mnuDecreaseFontSize.setText(QtGui.QApplication.translate("MainWindow", "&Decrease", None, QtGui.QApplication.UnicodeUTF8))

