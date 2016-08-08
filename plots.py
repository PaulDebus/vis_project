from pyqtgraph.Qt import QtGui, QtCore
import matplotlib.pyplot
import numpy as np
import pyqtgraph as pg
import viewbox as vb
scheme = 'summer'


def histogram(model, variables, parent=None, width=4, height=4):
	pg.setConfigOption('background', 0.98)
	pg.setConfigOption('foreground', 'k')

	pw = pg.PlotWidget()
	d =  model.data[:, variables]

	y,x = np.histogram(d, bins=10)
	color = tuple([255*i for i in list(matplotlib.pyplot.get_cmap(scheme)(0.5))])
	pw.plot(x, y, stepMode=True, fillLevel=0 ,pen='k', brush=color)
	pw.hideAxis('left')
	pw.hideAxis('bottom')
	return pw


def scatterplot(model, variables, parent=None, width=4, height=4):
	corr = model.corrmat[variables[0], variables[1]]
	color = tuple([255*i for i in list(correlationColor(corr))])
	pg.setConfigOption('background',color)
	pg.setConfigOption('foreground', 'k')
	pw = pg.PlotWidget(viewBox=vb.MyViewBox())

	t = model.data[:, variables[0]]
	s = model.data[:, variables[1]]

	s2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen('k'), pxMode=True)

	spots = [{'pos': [t[i],s[i]], 'data': 1, 'symbol': 'o', 'size': 1} for i in range(len(t))]
	s2.addPoints(spots)
	pw.hideAxis('left')
	pw.hideAxis('bottom')
	pw.addItem(s2)
	pw.getViewBox().setMouseMode(pg.ViewBox.RectMode)
	return pw


def correlationColor(corr):
	summer = matplotlib.pyplot.get_cmap(scheme)
	return summer(abs(corr))
