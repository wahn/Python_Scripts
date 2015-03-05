#!/usr/bin/env python

import sys

import PySide
from PySide.QtGui import QApplication
from PySide.QtGui import QMessageBox

# create the application object
app = QApplication(sys.argv)

# create a simple dialog box
msgBox = QMessageBox()
msgBox.setText("Hello World - using PySide version " + PySide.__version__)
msgBox.exec_()
