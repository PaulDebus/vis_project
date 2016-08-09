import pyqtgraph as pg
import matplotlib.pyplot
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

scheme='summer'

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
		color = correlationColor(0.5)
		pw.plot(x,y, stepMode=True, fillLevel=0, pen='k', brush=color)
		self.setWidget(pw)
		self.setWindowTitle("Histogramm: "+str(self.model.getIndexVariable(self.var1)))

class scattMDI(myMDI):

	def setup(self):
		pw = subScatter(self.model, [self.var1, self.var2])
		#pw = pg.PlotWidget()
                
		t = self.model.data[:, self.var1]
		s = self.model.data[:, self.var2]

		self.roi = pg.RectROI([np.mean(t)*0.95, np.mean(s)*0.95], [(max(t)-min(t))*0.1,(max(s)-min(s))*0.1], pen=pg.mkPen('r'))
		pw.addItem(self.roi)
		self.roi.setZValue(10)
		pw.roi = self.roi
		self.roi.hide()

		s2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen('k'), pxMode=True)

		spots = [{'pos': [t[i],s[i]], 'data': 1, 'symbol': 'o', 'size': 1} for i in range(len(t))]
		s2.addPoints(spots)
		pw.addItem(s2)
		self.setWidget(pw)
		self.setWindowTitle("ScatterPlot: "+str(self.model.getIndexVariable(self.var1))+ " / " +str(self.model.getIndexVariable(self.var2)))


def correlationColor(corr):
	summer = matplotlib.pyplot.get_cmap(scheme)
	return tuple([255*i for i in list(summer(abs(corr)))])

class subScatter(pg.PlotWidget):
	def __init__(self, model, variables):
		super(subScatter, self).__init__()
		self.model = model
		self.variables = variables
		self.selector = False
		self.roi = None
	def mousePressEvent(self,e):
		if e.button() == QtCore.Qt.RightButton:
			self.roi.hide()
			self.selector = not self.selector
			self.vb = self.getPlotItem().getViewBox()
			self.pos = self.vb.mapSceneToView(e.pos())
		else:
			super(subScatter, self).mousePressEvent(e)
	def mouseMoveEvent(self,e):
		if self.selector:
			if self.roi:
				epos = self.vb.mapSceneToView(e.pos())
				pos = [min(self.pos.x() , epos.x()) , min(self.pos.y(), epos.y())]
				self.roi.setPos(pos)
				size = [max(self.pos.x(), epos.x())-pos[0] , max(self.pos.y(), epos.y())-pos[1]]
				self.roi.setSize(size)
				self.roi.show()
		else:
			super(subScatter, self).mouseMoveEvent(e)
	def mouseReleaseEvent(self,e):
		if self.selector:
			self.selector = not self.selector
		else:
			super(subScatter, self).mouseReleaseEvent(e)
