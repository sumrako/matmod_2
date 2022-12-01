import numpy as np
from PyQt6.QtWidgets import QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QTableView
from model.tablemodel import NumpyModel


class ParamDialog(QDialog):
    def __init__(self, parent=None):
        super(ParamDialog, self).__init__(parent)
        self.parent = parent

        self.setWindowTitle('Общие параметры')
        self.setModal(True)
        self.step = QLineEdit()
        self.time = QLineEdit()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.sendForm)
        self.buttonBox.rejected.connect(self.reject)

        self.form = QFormLayout()
        self.form.setSpacing(20)

        self.form.addRow("&Шаг дифференцирования:", self.step)
        self.form.addRow("&Время моделирования:", self.time)
        self.form.addRow(self.buttonBox)

    def sendForm(self):
        self.parent.step = self.step
        self.parent.time = self.time

        self.close()


class KindDialog(QDialog):
    def __init__(self, count: int, parent=None):
        super(KindDialog, self).__init__(parent)
        self.parent = parent
        self.count = count

        self.setWindowTitle('Параметры видов')
        self.setModal(True)

        self.data = __generate_default_data()
        self.model = NumpyModel()

        self.table = QTableView()
        self.table.setModel(self.model)

    def __generate_default_data(self):
        count_of_popul = np.array()
        count_of_popul.append([i * 100 for i in range(1, self.count])

