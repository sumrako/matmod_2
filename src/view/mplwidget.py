from PyQt6.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from phaseportrait import PhasePortrait2D
from model.populations_model import dF


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


# class PhasePortraitCanvas(FigureCanvasQTAgg):
#     def __init__(self, a, b, c, d, parent=None):
#         fig, ax = PhasePortrait2D(dF, [-10, 10], dF_args={'a': a, 'b': b, 'c': c, 'd': d}).plot()
#         self.axes = ax
#         super(PhasePortraitCanvas, self).__init__(fig)


class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.setLayout(vertical_layout)

    # def phase_portrait_canvas(self, a, b, c, d):
    #     self.canvas = PhasePortraitCanvas(a, b, c, d, self)
    #
    #     vertical_layout = QVBoxLayout()
    #     vertical_layout.addWidget(self.canvas)
    #
    #     self.setLayout(vertical_layout)

    # def plot_canvas(self):
    #     self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
    #
    #     vertical_layout = QVBoxLayout()
    #     vertical_layout.addWidget(self.canvas)
    #
    #     self.setLayout(vertical_layout)

