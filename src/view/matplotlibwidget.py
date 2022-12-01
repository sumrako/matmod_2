from PyQt6.QtWidgets import QMainWindow, QInputDialog
from PyQt6.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random


class MatplotlibWidget(QMainWindow):

    def __init__(self):
        self.count_of_genus = None

        QMainWindow.__init__(self)
        loadUi("../assets/matmod2.ui", self)
        self.setWindowTitle("Модель популяции")

        self.menu_1.addAction("Новая система", self.open_count_dialog)
        self.menu_2.addAction("Общие параметры", self.open_param_dialog)
        self.menu_2.addAction("Параметры видов", self.open_genus_dialog)
        self.menu_3.addAction("Запуск модели", self.update_graph)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))


    def open_count_dialog(self):
        count_of_genus, ok = QInputDialog.getText(self, 'Количество видов', "Введите количество видов")
        if ok:
            self.count_of_genus = int(count_of_genus)


    def open_param_dialog(self):



    def update_graph(self):
        fs = 500
        f = random.randint(1, 100)
        ts = 1 / fs
        length_of_signal = 100
        t = np.linspace(0, 1, length_of_signal)

        cosinus_signal = np.cos(2 * np.pi * f * t)
        sinus_signal = np.sin(2 * np.pi * f * t)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.draw()