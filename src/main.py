from PyQt6.QtWidgets import *
from view.matplotlibwidget import MatplotlibWidget

import sys

import numpy as np
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView



app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec()
