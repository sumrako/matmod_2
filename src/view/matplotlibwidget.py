import pickle as pkl
from pathlib import Path

import numpy as np
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMainWindow, QInputDialog, QFileDialog
from PyQt6.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from model.populations_model import PopulationInteractionModel, generate_default_interactions_data, \
    generate_default_popul_data
from view.mydialogs import KindDialog, ParamDialog, AxesDialog, PhasePortraitDialog


class MatplotlibWidget(QMainWindow):
    def __init__(self):
        self.count_of_genus = 0
        self.N = None
        self.a = None
        self.B = None
        self.model = None
        self.N_matrix = None

        self.index = 0
        self.index_1 = 0
        self.index_2 = 1
        self.is_stopped = False
        self.step = 1
        self.time = 1000
        self.cur_time = 0
        self.t = np.array([0])
        self._plot_refs = None
        self.timer = QTimer()

        QMainWindow.__init__(self)
        loadUi("../assets/matmod2.ui", self)
        self.setWindowTitle("Модель популяции")

        self.menu.addAction("Новая система", self.open_count_dialog)
        self.menu.addAction("Сохранить систему", self.dump_system)
        self.menu.addAction("Открыть систему", self.load_system)
        self.menu_1.addAction("Продолжение и остановка системы", self.stop_system)
        self.menu_2.addAction("Общие параметры", self.open_param_dialog)
        self.menu_2.addAction("Параметры видов", self.open_genus_dialog)
        self.menu_3.addAction("Запуск модели", self.start_plot)
        self.menu_3.addAction("Фазовые портреты", self.phase_portrait)
        self.menu_3.addAction("Фазовая кривая", self.phase_curve)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        self.lineEdit.setText("0")
        self.lineEdit_2.setText("0")

        self.init_canvas(False)

        self.show()

    def init_canvas(self, is_curve=True):
        self.MplWidget.canvas.axes.cla()
        self.MplWidget.canvas.axes.grid()
        if is_curve:
            self.MplWidget.canvas.axes.set_xlim(0, 1000 if self.model.beginN is None else np.max(self.model.beginN) * 2)
        else:
            self.MplWidget.canvas.axes.set_xlim(0, self.time)
        self.MplWidget.canvas.axes.set_ylim(0, 1000 if self.N is None else np.max(self.model.beginN) * 2)
        self.MplWidget.canvas.axes.set_title('График численности')

    def dump_system(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Выберите директорию")
        if dir_name:
            path = Path(dir_name)
            pkl.dump(self.model, open(f'{str(path)}\\new_system.pkl', 'wb'), pkl.HIGHEST_PROTOCOL)

    def load_system(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Выберете файл системы",
            "D:\\",
            "Serialiazed file (*.pkl)"
        )
        if filename:
            path = Path(filename)
            self.model = pkl.load(open(str(path), 'rb'))
            print(self.model.B)

    def stop_system(self):
        if not self.is_stopped:
            self.timer.stop()
            self.is_stopped = True
        else:
            self.timer.start()
            self.is_stopped = False

    def phase_portrait(self):
        dialog = AxesDialog(self)
        dialog.exec()

        phase_dialog = PhasePortraitDialog(self, self.a[self.index_1],
                                           self.a[self.index_2],
                                           self.B[self.index_1, self.index_2],
                                           self.B[self.index_2, self.index_1])
        phase_dialog.exec()

    def plot(self, plot_func):
        self.MplWidget.canvas.axes.cla()
        self.cur_time = 0
        self.index = 0

        self.model.set_a(self.a)
        self.model.set_B(self.B)
        self.model.set_N(self.N)

        self._plot_refs = None
        self.N_matrix = self.model.get_N_matrix(self.time, self.step)
        self.t = np.array(range(0, self.time + self.step, self.step))

        # self.timer.destroyed()
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(plot_func)
        self.timer.start()

    def phase_curve(self):
        dialog = AxesDialog(self)
        dialog.exec()

        self.plot(self.update_phase_plot)

    def start_plot(self):
        self.plot(self.update_plot)

    def open_count_dialog(self):
        count_of_genus, ok = QInputDialog.getText(self, 'Количество видов', "Введите количество видов")
        if ok:
            self.count_of_genus = int(count_of_genus)
            popul_data = generate_default_popul_data(self.count_of_genus)
            self.N = popul_data[:, 0]
            self.a = popul_data[:, 1]
            self.B = generate_default_interactions_data(self.count_of_genus)
            self.model = PopulationInteractionModel(self.a, self.B, self.N)

            self.MplWidget.canvas.axes.set_xlim(0, self.time)
            self.MplWidget.canvas.axes.set_ylim(0, np.max(self.model.beginN) * 2)
            self.open_genus_dialog()

    def open_param_dialog(self):
        dialog = ParamDialog(self)
        dialog.exec()

    def open_genus_dialog(self):
        dialog = KindDialog(self)
        dialog.exec()

    def _plot_iter(self):
        if self.cur_time > self.time:
            self.timer.stop()
        else:
            self.lineEdit.setText(str(np.sum(self.N_matrix[:, self.index])))
            self.lineEdit_2.setText(str(self.cur_time))

    def update_phase_plot(self):
        self._plot_iter()
        if self._plot_refs is None:
            self.init_canvas(True)
            self._plot_refs = self.MplWidget.canvas.axes.plot(self.N_matrix[self.index_1, 0],
                                                              self.N_matrix[self.index_2, 0])
        else:
            for i in range(len(self._plot_refs)):
                self._plot_refs[i].set_xdata(self.N_matrix[self.index_2, :self.index])
                self._plot_refs[i].set_ydata(self.N_matrix[self.index_1, :self.index])

        self.cur_time += self.step
        self.index += 1
        self.MplWidget.canvas.draw()

    def update_plot(self):
        self._plot_iter()
        if self._plot_refs is None:
            self.init_canvas(False)
            self._plot_refs = self.MplWidget.canvas.axes.plot(self.t[0:1], [self.N_matrix.T[0, :2]])
        else:
            for i in range(len(self._plot_refs)):
                self._plot_refs[i].set_xdata(self.t[:self.index])
                self._plot_refs[i].set_ydata(self.N_matrix[i, :self.index])

        self.cur_time += self.step
        self.index += 1
        self.MplWidget.canvas.draw()
