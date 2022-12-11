from PyQt6.QtWidgets import QApplication

from view.matplotlibwidget import MatplotlibWidget

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec()
