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
		pw = subScatter(self, self.model, [self.var1, self.var2])
                
		t = self.model.data[:, self.var1]
		s = self.model.data[:, self.var2]

		self.roi = pg.RectROI([0,0],[1,1],pen=pg.mkPen('r'))
		pw.addItem(self.roi)
		self.roi.setZValue(10)
		pw.roi = self.roi
		pw.x = t
		pw.y = s
		self.roi.hide()
		
		self.setWindowTitle("ScatterPlot: "+str(self.model.getIndexVariable(self.var1))+ " / " +str(self.model.getIndexVariable(self.var2)))

		self.s2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen('k'), pxMode=True)
		self.malen()

		pw.addItem(self.s2)
		self.setWidget(pw)

	def malen(self):
		self.s2.clear()
		t = self.model.data[:, self.var1]
		s = self.model.data[:, self.var2]
		selection = self.model.selection
		spots = []
		for i in range(len(t)):
			if i in selection:
				pen = pg.mkPen('r')
				size = 4
			else:
				pen = pg.mkPen('k')
				size = 1
			spots.append({'pos': [t[i],s[i]], 'data': 1, 'symbol': 'o', 'size': size, 'pen': pen})
		self.s2.addPoints(spots)


def correlationColor(corr):
	summer = matplotlib.pyplot.get_cmap(scheme)
	return tuple([255*i for i in list(summer(abs(corr)))])

class subScatter(pg.PlotWidget):
	def __init__(self, parent, model, variables):
		super(subScatter, self).__init__()
		self.model = model
		self.variables = variables
		self.selector = False
		self.roi = None
		self.x = []
		self.y = []
		self.parent = parent
	def mousePressEvent(self,e):
		if e.button() == QtCore.Qt.RightButton:
			self.roi.hide()
			self.model.resetSelection()
			self.parent.malen()
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
				# get ROI shape in coordinate system of the scatter plot
				roiShape = self.roi.mapToItem(self.getPlotItem(), self.roi.shape())
				# Get list of all points inside shape
				selected = [i for i in range(len(self.x)) if roiShape.contains(self.vb.mapViewToScene(QtCore.QPoint(self.x[i], self.y[i])))]
				self.model.setSelection(selected)
				self.parent.malen()
		else:
			super(subScatter, self).mouseMoveEvent(e)
	def mouseReleaseEvent(self,e):
		if self.selector:
			self.selector = not self.selector
		else:
			super(subScatter, self).mouseReleaseEvent(e)
