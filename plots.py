from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

scheme = 'summer'


def histogram(model, variables, parent=None, width=4, height=4):
    pw = pg.ScatterPlotWidget()
    pw.setData(model.data)
    pw.setFields(variables)
    return pw


def scatterplot(model, variables, parent=None, width=4, height=4):
    pw = pg.PlotWidget()
#    pw.setData(model.data)
 #   pw.setFields(variables)
    n = 300
    s2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen('w'), pxMode=True)
    pos = np.random.normal(size=(2,n), scale=1e-5)
    spots = [{'pos': pos[:,i], 'data': 1, 'brush':pg.intColor(i, n), 'symbol': 'o', 'size': 1} for i in range(n)]
    s2.addPoints(spots)
    pw.addItem(s2)
    return pw


def correlationColor(corr):
    summer = matplotlib.pyplot.get_cmap(scheme)
    return summer(abs(corr))
