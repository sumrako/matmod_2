import numpy as np
from PyQt6.QtCore import QAbstractTableModel, Qt


class NumpyModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data[index.row(), index.column()]
                return str(value)

    def numpy_data(self) -> np.ndarray:
        return np.array(self._data)

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            try:
                value = int(value)
            except ValueError:
                return False
            self._data[index.row(), index.column()] = value
            return True
        return False

    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
