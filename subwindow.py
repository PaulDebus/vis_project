import pyqtgraph as pg
import matplotlib.pyplot
from pyqtgraph.Qt import QtGui
import numpy as np

class myMDI(QtGui.QMdiSubWindow):
    def __init__(self, model, var1, var2):
        super(QtGui.QMdiSubWindow, self).__init__()
        self.model = model
        self.var1 = var1
        self.var2 = var2
        self.setup()

class histMDI(myMDI):
    def setup(self):
        pg.setConfigOption('foreground', 'k')
        pw = pg.PlotWidget()
        d = self.model.data[:, self.var1]

        y,x = np.histogram(d, bins=25)
        color = (100,100,255,255)
        pw.plot(x,y, stepMode=True, fillLevel=0, pen='k', brush=color)
        self.setWidget(pw)

class scattMDI(myMDI):

    def setup(self):
        corr = self.model.corrmat[self.var1, self.var2]
        #color = tuple([255*i for i in list(matplotlib.pyplot.get_cmap(scheme)(corr))])
        #pg.setConfigOption('background',color)
        #pg.setConfigOption('foreground', 'k')
        pw = pg.PlotWidget()

        t = self.model.data[:, self.var1]
        s = self.model.data[:, self.var2]

        s2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen('k'), pxMode=True)

        spots = [{'pos': [t[i],s[i]], 'data': 1, 'symbol': 'o', 'size': 1} for i in range(len(t))]
        s2.addPoints(spots)
        pw.addItem(s2)
        self.setWidget(pw)


def correlationColor(corr):
	summer = matplotlib.pyplot.get_cmap(scheme)
	return summer(abs(corr))
