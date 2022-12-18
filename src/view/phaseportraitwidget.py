from PyQt6.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from phaseportrait import PhasePortrait2D
from model.populations_model import dF, PopulationInteractionModel
from matplotlib.figure import Figure


class PhasePortraitCanvas(FigureCanvasQTAgg):
    def __init__(self, a, b, c, d, parent=None):
        fig, ax = PhasePortrait2D(dF, [0, 200], dF_args={'a': a, 'b': b, 'c': c, 'd': d},
                                  Title="Фазовый портрет взаиодействующих популяций", xlabel="M", ylabel="N").plot()
        self.axes = ax
        super(PhasePortraitCanvas, self).__init__(fig)


class PhasePortraitWidget(QWidget):
    def __init__(self, a, b, c, d, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = PhasePortraitCanvas(a, b, c, d)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.setLayout(vertical_layout)
        self.canvas.draw()
