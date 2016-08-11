from pyqtgraph.Qt import QtGui, QtCore
import matplotlib.pyplot
import numpy as np
import pyqtgraph as pg
import viewbox as vb
scheme = 'summer'

def colorBar(width, height):
	#ColorLegend for CorrelationCoefficient in Matrix
	center = QtGui.QWidget()
	center.lay = QtGui.QVBoxLayout(center)
	title = QtGui.QLabel("Coefficient of \n Correlation")
	center.lay.addWidget(title)
	hor = QtGui.QWidget()
	center.lay.addWidget(hor)
	horlay = QtGui.QHBoxLayout()
	hor.setLayout(horlay)
	center.lay.addWidget(hor)
	l = QtGui.QLabel()
	l.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
	'''
	l.pixmap	= QtGui.QPixmap (QtCore.QSize(width,height))		
	l.painter	= QtGui.QPainter (l.pixmap)		
	gradient 	= QtGui.QLinearGradient(QtCore.QPointF(l.pixmap.rect().bottomLeft()),
				QtCore.QPointF(l.pixmap.rect().topLeft()))		
				
	gradient.setColorAt(0,	QtGui.QColor(*correlationColor(1)))
	gradient.setColorAt(1,	QtGui.QColor(*correlationColor(0.5)))
	gradient.setColorAt(2,	QtGui.QColor(*correlationColor(0))		)
			
	brush 	= QtGui.QBrush(gradient)				
	l.painter.fillRect( QtCore.QRectF(0, 0, width, height),brush)
	'''
	l.pixmap=QtGui.QPixmap(scheme+'.jpg')
	l.setPixmap(l.pixmap)
	horlay.addWidget(l)
	lab = QtGui.QWidget()
	labels = QtGui.QVBoxLayout()
	lab.setLayout(labels)
	horlay.addWidget(lab)
	labels.addWidget(QtGui.QLabel('1'))
	labels.addStretch()
	labels.addWidget(QtGui.QLabel('0'))
	return center


def histogram(model, variables, parent=None, width=4, height=4):
	#creates histogramm
	pg.setConfigOption('background', 0.98)
	pg.setConfigOption('foreground', 'k')
	pw = pg.PlotWidget()
	d =	model.data[:, variables]
	y,x = np.histogram(d, bins=10)
	color = correlationColor(0.5)
	pw.plot(x, y, stepMode=True, fillLevel=0 ,pen='k', brush=color)
	pw.hideAxis('left')
	pw.hideAxis('bottom')
	pw.hideButtons()
	pw.setMouseEnabled(False,False)
	return pw

class myScatter(pg.PlotWidget):
	#scatterplot class for mouse functionality
	def __init__(self, parent, model, variables):
		super(myScatter, self).__init__()
		self.parent = parent
		self.model = model
		self.variables = variables
	def mousePressEvent(self,e):
		self.model.setSelectedVariables(self.variables[1], self.variables[0])
		self.parent.showDataBoxes()
	def mouseMoveEvent(self,e):
		pass
	def mouseReleaseEvent(self,e):
		pass

def scatterplot(model, variables, parent=None, width=4, height=4):
	#creates scatterplot
	corr = model.corrmat[variables[0], variables[1]]
	color = correlationColor(corr)
	pg.setConfigOption('background',color)
	pg.setConfigOption('foreground', 'k')
	pw = myScatter(parent, model, variables)
	t = model.data[:, variables[0]]
	s = model.data[:, variables[1]]

	s2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen('k'), pxMode=True)

	spots = [{'pos': [t[i], s[i]], 'data': 1, 'symbol': 'o', 'size': 1} for i in range(len(t))]
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
