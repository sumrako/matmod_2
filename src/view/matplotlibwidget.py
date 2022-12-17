from PyQt6.QtWidgets import QMainWindow, QInputDialog, QVBoxLayout
from PyQt6.uic import loadUi
from PyQt6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from view.mydialogs import KindDialog, ParamDialog, AxesDialog, PhaseDialog
from model.populations_model import PopulationInteractionModel, generate_default_interactions_data, \
    generate_default_popul_data
from view.phaseportraitwidget import PhasePortraitCanvas

import numpy as np


class MatplotlibWidget(QMainWindow):
    def __init__(self):
        self.count_of_genus = 2
        popul_data = generate_default_popul_data(self.count_of_genus)

        self.popul_count_data = popul_data[:, 0]
        self.alpha_data = popul_data[:, 1]
        self.interactions_data = generate_default_interactions_data(self.count_of_genus)

        self.index_1 = 0
        self.index_2 = 1
        self.is_stopped = False
        self.step = 1
        self.time = 1000
        self.cur_time = 0
        self.t = np.array([0])

        QMainWindow.__init__(self)
        loadUi("../assets/matmod2.ui", self)
        self.setWindowTitle("Модель популяции")

        self.menu.addAction("Новая система", self.open_count_dialog)
        self.menu_1.addAction("Остановка системы", self.stop_system)
        self.menu_1.addAction("Сброс системы", self.reset_system)
        self.menu_2.addAction("Общие параметры", self.open_param_dialog)
        self.menu_2.addAction("Параметры видов", self.open_genus_dialog)
        self.menu_3.addAction("Запуск модели", self.start_plot)
        self.menu_3.addAction("Фазовые портреты", self.phase_portrait)
        self.menu_3.addAction("Базовые графики", self.base_plot)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        self.lineEdit.setText(str(np.sum(self.popul_count_data)))
        self.lineEdit_2.setText(str(self.cur_time))

        self.model = PopulationInteractionModel(self.alpha_data, self.interactions_data, self.popul_count_data)
        self.N_matrix = np.array([self.popul_count_data]).T

        self.init_canvas()
        self._plot_refs = None
        self.timer = QTimer()

        self.show()

    def init_canvas(self):
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.grid()
        self.MplWidget.canvas.axes.set_xlim(0, self.time)
        self.MplWidget.canvas.axes.set_ylim(0, np.max(self.popul_count_data) * 2)
        self.MplWidget.canvas.axes.set_title('График численности')

    def stop_system(self):
        self.timer.stop()
        self.is_stopped = True

    def reset_system(self):
        pass

    def phase_portrait(self):
        self.is_stopped = False
        dialog = AxesDialog(self)
        dialog.exec()

        dialog = PhaseDialog(self)
        dialog.PhasePortraitWidget.canvas = PhasePortraitCanvas(self.alpha_data[self.index_1],
                                                                self.alpha_data[self.index_2],
                                                                self.interactions_data[self.index_1, self.index_2],
                                                                self.interactions_data[self.index_2, self.index_1],
                                                                dialog)
        dialog.exec()

    def base_plot(self):
        pass
        # self.MplWidget.canvas.plot_canvas()
        # self.init_canvas()

    def start_plot(self):
        if not self.is_stopped:
            self.MplWidget.canvas.axes.cla()
            self.cur_time = 0
            self.model = PopulationInteractionModel(self.alpha_data, self.interactions_data, self.popul_count_data)
            self._plot_refs = None
            self.N_matrix = np.array([self.popul_count_data]).T
            self.t = np.array([0])

        self.timer.setInterval(1)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def open_count_dialog(self):
        self.is_stopped = False
        count_of_genus, ok = QInputDialog.getText(self, 'Количество видов', "Введите количество видов")
        if ok:
            self.count_of_genus = int(count_of_genus)
            self.open_genus_dialog()

    def open_param_dialog(self):
        self.is_stopped = False
        dialog = ParamDialog(self)
        dialog.exec()

    def open_genus_dialog(self):
        self.is_stopped = False
        dialog = KindDialog(self)
        dialog.exec()

    def update_plot(self):
        if self.cur_time > self.time:
            self.timer.stop()

        self.cur_time += self.step
        N_col = np.array([self.model.get_N_after_step()]).T

        self.lineEdit.setText(str(np.sum(N_col)))
        self.lineEdit_2.setText(str(self.cur_time))

        self.N_matrix = np.append(self.N_matrix, N_col, axis=1)
        self.t = np.append(self.t, self.cur_time)

        if self._plot_refs is None:
            self.init_canvas()
            self._plot_refs = self.MplWidget.canvas.axes.plot(self.t, self.N_matrix.T)
        else:
            for i in range(len(self._plot_refs)):
                self._plot_refs[i].set_xdata(self.t)
                self._plot_refs[i].set_ydata(self.N_matrix[i])

        self.MplWidget.canvas.draw()
