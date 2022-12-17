from PyQt6.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from phaseportrait import PhasePortrait2D
from model.populations_model import dF


class PhasePortraitCanvas(FigureCanvasQTAgg):
    def __init__(self, a, b, c, d, parent=None):
        # M0 = a / (-c)
        #         # N0 = (-b) / d
        #         # # print(a, b, c, d)
        #         # # print(M0, N0)
        #         #
        #         # axisY = [M0 - 100, M0 + 100]
        #         # axisX = [N0 - 100, N0 + 100]
        fig, ax = PhasePortrait2D(dF, [-10, 10], dF_args={'a': a, 'b': b, 'c': c, 'd': d}).plot()
        self.axes = ax
        super(PhasePortraitCanvas, self).__init__(fig)


class PhasePortraitWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = PhasePortraitCanvas(0.01, 0.01, 0.0001, 0.0001, self)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.setLayout(vertical_layout)
