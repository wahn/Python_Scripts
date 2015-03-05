#!/usr/bin/env python

import sys

import PySide
from PySide.QtGui import QApplication, QCalendarWidget

class Window(QCalendarWidget):
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
