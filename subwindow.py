import pyqtgraph as pg
import matplotlib.pyplot
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
from scipy import stats as st

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

class CoRMDI(myMDI):
	def setup(self):
		pg.setConfigOption('foreground', 'k')
		pw = pg.PlotWidget()
		d = self.model.data[:, self.var1]
		sts=[]
		for i in range(self.model.inputNames):
			sts.append(1-)
		color = correlationColor(0.5)
		pw.plot(x,y, stepMode=True, fillLevel=0, pen='k', brush=color)
		self.setWidget(pw)
		self.setWindowTitle("Histogramm: "+str(self.model.getIndexVariable(self.var1)))


class MeanStdMDI(myMDI):
	def setup(self):
		pw = pg.PlotWidget()
		#num of steps
		bin=20
		#get aata
		t = self.model.data[:, self.var1]
		s = self.model.data[:, self.var2]
		#generate 'histogram' with mean values, std and edges 
		mean,edges,c=st.binned_statistic(t,s,statistic='mean',bins=bin)
		#max,edges,c=st.binned_statistic(t,s,statistic=np.amax,bins=bin)
		#min,edges,c=st.binned_statistic(t,s,statistic=np.amin,bins=bin)
		std,edges,c=st.binned_statistic(t,s,statistic=np.std,bins=bin)
		#creates upper and lower bound
		min=[]
		max=[]
		for i in range(0,len(mean)):
			min.append(mean[i]-std[i])
			max.append(mean[i]+std[i])
		#transfer edges to midpoints
		midpoints=[]
		old=edges[0]
		for i in edges:
			midpoints.append((old+i)/2)
			old=i
		midpoints.pop(0)
		#plot lines
		minPlot=pg.PlotDataItem(midpoints, min, pen=pg.mkPen('w'))
		meanPlot=pg.PlotDataItem(midpoints, mean, pen=pg.mkPen('k',width=2))
		maxPlot=pg.PlotDataItem(midpoints, max, pen=pg.mkPen('w'))
		#generate fill and fillcolor
		colorMin=correlationColor(0.33)
		colorMin=tuple([colorMin[0],colorMin[1],colorMin[2],150])
		fill1=pg.FillBetweenItem(minPlot, meanPlot, brush=pg.mkBrush(colorMin))
		colorMax=correlationColor(0.66)
		colorMax=tuple([colorMax[0],colorMax[1],colorMax[2],150])
		fill2=pg.FillBetweenItem(meanPlot, maxPlot, brush=pg.mkBrush(colorMax))
		#add all to graph
		pw.addItem(minPlot)
		pw.addItem(meanPlot)
		pw.addItem(maxPlot)
		pw.addItem(fill1)
		pw.addItem(fill2)
		self.setWidget(pw)
		self.setWindowTitle("Mean- and StandardDeviationPlot: "+str(self.model.getIndexVariable(self.var1))+ " / " +str(self.model.getIndexVariable(self.var2)))

class TextMDI(myMDI):

	def setup(self):
		pw = QtGui.QWidget()
		t = self.model.data[:, self.var1]
		s = self.model.data[:, self.var2]
		#stats from both variables
		table1=("<table>"+
			"<th align=\"left\">"+self.model.getIndexVariable(self.var1) + " and " + self.model.getIndexVariable(self.var2)+"</th>"+
			"<tr><td>Number of Datapoints:</td><td>{}".format(len(t))+"</td></tr>"+
			"<tr><td>Correlation Coefficient:</td><td>{0:.5f}".format(self.model.corrmat[self.var1,self.var2])+"</td></tr>"+
			"</table>")
		#stats from variable 1
		table2=("<table>"+
			"<th align=\"left\">"+self.model.getIndexVariable(self.var1)+"</th>"+
			"<tr><td>Min: <\td><td>{0:.5f}".format(self.model.stats[self.var1].min)+"</td></tr>"+
			"<tr><td>Max: <\td><td>{0:.5f}".format(self.model.stats[self.var1].max)+"</td></tr>"+
			"<tr><td>Mean: <\td><td>{0:.5f}".format(self.model.stats[self.var1].mean)+"</td></tr>"+
			"<tr><td>Median: <\td><td>{0:.5f}".format(self.model.stats[self.var1].median)+"</td></tr>"+
			"<tr><td>Standard Deviation: <\td><td>{0:.5f}".format(self.model.stats[self.var1].std)+"</td></tr>"+
			"<tr><td>Variance: <\td><td>{0:.5f}".format(self.model.stats[self.var1].var)+"</td></tr>"+
			"</table>")
		#stats from variable 2
		table3=("<table>"+
			"<th align=\"left\">"+self.model.getIndexVariable(self.var2)+"</th>"+
			"<tr><td>Min: <\td><td>{0:.5f}".format(self.model.stats[self.var2].min)+"</td></tr>"+
			"<tr><td>Max: <\td><td>{0:.5f}".format(self.model.stats[self.var2].max)+"</td></tr>"+
			"<tr><td>Mean: <\td><td>{0:.5f}".format(self.model.stats[self.var2].mean)+"</td></tr>"+
			"<tr><td>Median: <\td><td>{0:.5f}".format(self.model.stats[self.var2].median)+"</td></tr>"+
			"<tr><td>Standard Deviation: <\td><td>{0:.5f}".format(self.model.stats[self.var2].std)+"</td></tr>"+
			"<tr><td>Variance: <\td><td>{0:.5f}".format(self.model.stats[self.var2].var)+"</td></tr>"+
			"</table>")
		#print labels
		labels=[]
		labels.append(QtGui.QLabel("<h2>Statistical Data from: </h2>"))
		labels.append(QtGui.QLabel(table1))
		labels.append(QtGui.QLabel(table2))
		labels.append(QtGui.QLabel(table3))
		vbox = QtGui.QVBoxLayout()
		for i in labels:
			vbox.addWidget(i)
		pw.setLayout(vbox)
		self.setWidget(pw)

class scattMDI(myMDI):

	def setup(self):
		self.roi = pg.RectROI([0,0],[1,1],pen=pg.mkPen('r'))
		pw = subScatter(self, self.model, [self.var1, self.var2], self.roi)
		t = self.model.data[:, self.var1]
		s = self.model.data[:, self.var2]
		self.model.subscribeSelection(self)

		pw.addItem(self.roi)
		self.roi.setZValue(10)
		pw.x = t
		pw.y = s
		self.roi.hide()
		
		self.setWindowTitle("ScatterPlot: "+str(self.model.getIndexVariable(self.var1))+ " / " +str(self.model.getIndexVariable(self.var2)))

		self.s2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen('k'), pxMode=True)
		self.refresh()

		pw.addItem(self.s2)
		self.setWidget(pw)

	def refresh(self):
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
	def __init__(self, parent, model, variables, roi):
		super(subScatter, self).__init__()
		self.model = model
		self.variables = variables
		self.selector = False
		self.roi = roi
		self.x = []
		self.y = []
		self.parent = parent
		self.roi.sigRegionChangeFinished.connect(self.select)
	def mousePressEvent(self,e):
		if e.button() == QtCore.Qt.RightButton:
			self.roi.hide()
			self.roi.sigRegionChangeFinished.disconnect()
			self.model.resetSelection()
			self.selector = not self.selector
			self.vb = self.getPlotItem().getViewBox()
			self.pos = self.vb.mapSceneToView(e.pos())
		else:
			super(subScatter, self).mousePressEvent(e)
	def mouseMoveEvent(self,e):
		if self.selector:
			epos = self.vb.mapSceneToView(e.pos())
			pos = [min(self.pos.x() , epos.x()) , min(self.pos.y(), epos.y())]
			self.roi.setPos(pos)
			size = [max(self.pos.x(), epos.x())-pos[0] , max(self.pos.y(), epos.y())-pos[1]]
			self.roi.setSize(size)
			self.roi.show()
		else:
			super(subScatter, self).mouseMoveEvent(e)

	def select(self):
				# get ROI shape in coordinate system of the scatter plot
				roiShape = self.roi.mapToItem(self.getPlotItem(), self.roi.shape())
				# Get list of all points inside shape
				def contains(x,y):
						rect = roiShape.controlPointRect()
						bl = rect.bottomLeft()
						tr = rect.topRight()
						bl = self.vb.mapSceneToView(bl)
						tr = self.vb.mapSceneToView(tr)
						bottom = bl.y()
						left = bl.x()
						right = tr.x()
						top = tr.y()
						if x > left:
							if x < right:
								if y > bottom:
									if y < top:
										return True
						return False
				selected = [i for i in range(len(self.x)) if contains(self.x[i], self.y[i])]
				self.model.setSelection(selected)
	def mouseReleaseEvent(self,e):
		if self.selector:
			self.selector = not self.selector
			self.select()
			self.roi.sigRegionChangeFinished.connect(self.select)
		else:
			super(subScatter, self).mouseReleaseEvent(e)
