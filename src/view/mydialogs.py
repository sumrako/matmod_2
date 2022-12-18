import numpy as np
from PyQt6.QtWidgets import QDialog, QLineEdit, QFormLayout, QDialogButtonBox,\
    QTableView, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt6.QtCore import pyqtSlot
from model.tablemodel import NumpyModel
from model.populations_model import generate_default_popul_data, generate_default_interactions_data
from PyQt6.uic import loadUi
from view.phaseportraitwidget import PhasePortraitWidget


class ParamDialog(QDialog):
    def __init__(self, parent=None):
        super(ParamDialog, self).__init__(parent)
        self.parent = parent

        self.setWindowTitle('Общие параметры')
        self.step = QLineEdit(self)
        self.time = QLineEdit(self)
        self.step.setText("1")
        self.time.setText("1000")

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.accepted.connect(self.sendForm)
        self.buttonBox.rejected.connect(self.reject)

        self.form = QFormLayout(self)
        self.form.setSpacing(20)

        self.form.addRow("&Шаг дифференцирования:", self.step)
        self.form.addRow("&Время моделирования:", self.time)
        self.form.addRow(self.buttonBox)

    def sendForm(self):
        self.parent.step = int(self.step.text())
        self.parent.time = int(self.time.text())

        self.close()


class AxesDialog(QDialog):
    def __init__(self, parent=None):
        super(AxesDialog, self).__init__(parent)
        self.parent = parent

        self.setWindowTitle("Выберете индексы взаимодействующих популяций")
        page_layout = QVBoxLayout(self)
        first_layout = QHBoxLayout()
        second_layout = QHBoxLayout()
        self.box_1 = QComboBox()
        self.box_2 = QComboBox()

        label1 = QLabel("Индекс первой популяции")
        label2 = QLabel("Индекс второй популяции")

        index_items = [str(i) for i in range(parent.count_of_genus)]
        self.box_1.addItems(index_items)
        self.box_2.addItems(index_items)

        input_button = QPushButton("Ввести")
        input_button.clicked.connect(self.input)

        first_layout.addWidget(label1)
        first_layout.addWidget(self.box_1)
        second_layout.addWidget(label2)
        second_layout.addWidget(self.box_2)

        page_layout.addLayout(first_layout)
        page_layout.addLayout(second_layout)
        page_layout.addWidget(input_button)

    @pyqtSlot()
    def input(self):
        index1 = self.box_1.currentIndex()
        index2 = self.box_2.currentIndex()
        if index1 == index2:
            self.close()
            return
        self.parent.index_1 = self.box_1.currentIndex()
        self.parent.index_2 = self.box_2.currentIndex()

        self.close()


class PhasePortraitDialog(QDialog):
    def __init__(self, parent, a, b, c, d):
        super(PhasePortraitDialog, self).__init__(parent)
        # Load the dialog's GUI
        # loadUi("../assets/dialog.ui", self)
        self.setWindowTitle("Фазовой портрет")
        self.setFixedSize(640, 480)
        self.phase_widget = PhasePortraitWidget(a, b, c, d, parent=self)



class KindDialog(QDialog):
    def __init__(self, parent=None):
        super(KindDialog, self).__init__(parent)
        self.parent = parent

        page_layout = QHBoxLayout(self)
        popul_layout = QVBoxLayout()
        interactions_layout = QVBoxLayout()
        button_layout = QVBoxLayout()

        self.count = parent.count_of_genus

        self.setWindowTitle('Параметры видов')

        popul_data = generate_default_popul_data(self.count)
        self.popul_model = NumpyModel(popul_data)
        self.popul_table = QTableView()
        self.popul_table.setModel(self.popul_model)

        interaction_data = generate_default_interactions_data(self.count)
        self.interaction_model = NumpyModel(interaction_data)
        self.interaction_table = QTableView()
        self.interaction_table.setModel(self.interaction_model)

        input_button = QPushButton("Ввести")
        input_button.clicked.connect(self.input)
        button_layout.addWidget(input_button)

        popul_layout.addWidget(QLabel("Численность популяции i-ого вида"))
        popul_layout.addWidget(self.popul_table)

        interactions_layout.addWidget(QLabel("Коэффициенты взаимодействия популяций"))
        interactions_layout.addWidget(self.interaction_table)

        page_layout.addLayout(popul_layout)
        page_layout.addLayout(interactions_layout)
        page_layout.addLayout(button_layout)

    @pyqtSlot()
    def input(self):
        popul_data = self.popul_table.model().numpy_data()
        self.parent.a = popul_data[:, 1]
        self.parent.N = np.int_(popul_data[:, 0])
        self.parent.B = self.interaction_table.model().numpy_data()

        self.parent.model.set_a(popul_data[:, 1])
        self.parent.model.set_N(popul_data[:, 0])
        self.parent.model.set_B(self.interaction_table.model().numpy_data())
        self.close()


