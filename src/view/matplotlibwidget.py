from PyQt6.QtWidgets import QMainWindow, QInputDialog
from PyQt6.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from view.mydialogs import KindDialog, ParamDialog
from model.populations_model import PopulationInteractionModel, generate_default_interactions_data,\
    generate_default_popul_data

import numpy as np


class MatplotlibWidget(QMainWindow):
    def __init__(self):

        self.count_of_genus = 2
        popul_data = generate_default_popul_data(self.count_of_genus)
        self.popul_count_data = popul_data[:, 1]
        self.alpha_data = popul_data[:, 0]
        self.interactions_data = generate_default_interactions_data(self.count_of_genus)
        self.model = PopulationInteractionModel(self.alpha_data, self.interactions_data, self.popul_count_data)
        self.step = 1
        self.time = 1000

        QMainWindow.__init__(self)
        loadUi("../assets/matmod2.ui", self)
        self.setWindowTitle("Модель популяции")

        self.menu.addAction("Новая система", self.open_count_dialog)
        self.menu_2.addAction("Общие параметры", self.open_param_dialog)
        self.menu_2.addAction("Параметры видов", self.open_genus_dialog)
        self.menu_3.addAction("Запуск модели", self.start_graph)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

    def open_count_dialog(self):
        count_of_genus, ok = QInputDialog.getText(self, 'Количество видов', "Введите количество видов")
        if ok:
            self.count_of_genus = int(count_of_genus)

    def open_param_dialog(self):
        dialog = ParamDialog(self)
        dialog.exec()

    def open_genus_dialog(self):
        dialog = KindDialog(self)
        dialog.exec()

    def start_graph(self):
        cur_time = 0
        t = np.array([0])
        N_matrix = np.array(self.popul_count_data.T)
        self.model = PopulationInteractionModel(self.alpha_data, self.interactions_data, self.popul_count_data)

        while cur_time <= self.time:
            cur_time += self.step
            N_col = self.model.get_N_after_step()

            self.lineEdit.setText(str(np.sum(N_col)))
            self.lineEdit_2.setText(str(cur_time))

            print(N_matrix)
            print(N_col)

            np.append(N_matrix, N_col, axis=1)
            np.append(t, cur_time)

            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.axes.xlim(0, self.time)
            self.MplWidget.canvas.axes.ylim(0, np.max(self.popul_count_data) * 2)

            for row in N_matrix:
                self.MplWidget.canvas.axes.plot(t, row)

            self.MplWidget.canvas.axes.set_title('График численности')
            self.MplWidget.canvas.draw()
