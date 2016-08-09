from pyqtgraph.Qt import QtGui, QtCore
import matplotlib.pyplot
import numpy as np
import pyqtgraph as pg
import viewbox as vb
import colorBar as cb
scheme = 'summer'

def colorBar(model, parent=None, width=4, height=4):
	pw = pg.PlotWidget()
	summer = matplotlib.pyplot.get_cmap(scheme)
	# make colormap
	stops = np.r_[0, 0.5, 1.0]
	colors = np.array([summer(i) for i in stops])
	cm = pg.ColorMap(stops, colors)
	cob = cb.ColorBar(cm, width, height, label='Correlation')
	#cob.setRotation(180)
	#cob.setScale(0.5)
	pw.addItem(cob)
	pw.hideAxis('left')
	pw.hideAxis('bottom')
	pw.hideButtons()
	#pw.setMouseEnabled(False,False)
	'''pw=pg.GradientWidget()
	cm=pg.GradientEditorItem()
	stops = np.r_[0, 0.5, 1.0]
	colors = np.array([correlationColor(i) for i in stops])
	cm = pg.ColorMap(stops, colors)'''
	return pw

def histogram(model, variables, parent=None, width=4, height=4):

	pg.setConfigOption('background', 0.98)
	pg.setConfigOption('foreground', 'k')

	pw = pg.PlotWidget()
	d =  model.data[:, variables]


	y,x = np.histogram(d, bins=10)
	color = correlationColor(0.5)
	pw.plot(x, y, stepMode=True, fillLevel=0 ,pen='k', brush=color)
	pw.hideAxis('left')
	pw.hideAxis('bottom')
	pw.hideButtons()
	pw.setMouseEnabled(False,False)
	return pw

class myScatter(pg.PlotWidget):
	def __init__(self, parent, model, variables):
		super(myScatter, self).__init__()
		self.parent = parent
		self.model = model
		self.variables = variables
		#self.variables[0] = len(model.activeVariables)+1 - self.variables[0]
	def mousePressEvent(self,e):
			self.model.setSelectedVariables(self.variables[1], self.variables[0])
			self.parent.showDataBoxes()
	def mouseMoveEvent(self,e):
		pass
	def mouseReleaseEvent(self,e):
		pass

def scatterplot(model, variables, parent=None, width=4, height=4):
	corr = model.corrmat[variables[0], variables[1]]
	color = correlationColor(corr)
	pg.setConfigOption('background',color)
	pg.setConfigOption('foreground', 'k')
	pw = myScatter(parent, model, variables)
	t = model.data[:, variables[0]]
	s = model.data[:, variables[1]]

	s2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen('k'), pxMode=True)

	spots = [{'pos': [t[i],s[i]], 'data': 1, 'symbol': 'o', 'size': 1} for i in range(len(t))]
	s2.addPoints(spots)
	pw.hideAxis('left')
	pw.hideAxis('bottom')
	pw.hideButtons()
	pw.addItem(s2)
	pw.setMouseEnabled(False,False)

	return pw


def correlationColor(corr):
	summer = matplotlib.pyplot.get_cmap(scheme)
	return tuple([255*i for i in list(summer(abs(corr)))])


