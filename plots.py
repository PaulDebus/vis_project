import matplotlib.pyplot
from matplotlib.figure import Figure
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

scheme='summer'

class MyMplCanvas(FigureCanvas):

    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(
            self,
            model,
            variables,
            labels=False,
            parent=None,
            width=5,
            height=4,
            dpi=100):
        self.model = model
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        if not labels:
            self.axes.tick_params(
                axis='both',
                labelbottom='off',
                labelleft='off')
            fig.subplots_adjust(
                left=0.01,
                bottom=0.01,
                right=0.99,
                top=0.99,
                wspace=None,
                hspace=None)

        self.compute_initial_figure(variables)

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class histogram(MyMplCanvas):

    def compute_initial_figure(self, variables):
        x = self.model.data[:, variables]
        self.axes.hist(x, 20, normed=1, color=matplotlib.pyplot.get_cmap(scheme)(0.5))


class scatterplot(MyMplCanvas):

    def compute_initial_figure(self, variables):
        t = self.model.data[:, variables[0]]
        s = self.model.data[:, variables[1]]
        self.axes.scatter(t, s, c='black',marker='.',alpha=0.2)
        corr = self.model.corrmat[variables[0], variables[1]]
        self.axes.set_axis_bgcolor(correlationColor(corr))


def correlationColor(corr):
    summer =  matplotlib.pyplot.get_cmap(scheme)
    return summer(abs(corr))
