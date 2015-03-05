#!/usr/bin/env python

import sys

import PySide
from PySide.QtCore import Qt
from PySide.QtGui  import QApplication, QCalendarWidget

class Window(QCalendarWidget):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.setFirstDayOfWeek(Qt.DayOfWeek.Monday)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
