import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
from scipy import stats as st
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

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

class Radar(object):
	def __init__(self, fig, titles, labels, rect=None):
		if rect is None:
			rect = [0.1, 0.1, 0.8, 0.8]
		self.n = len(titles)
		self.angles = np.arange(0,360, 360.0/self.n)
		self.axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i) 
						 for i in range(self.n)]
		self.ax = self.axes[0]
		self.ax.set_thetagrids(self.angles, labels=titles, fontsize=14)
		for ax in self.axes[1:]:
			ax.patch.set_visible(False)
			ax.grid("off")
			ax.xaxis.set_visible(False)
		for ax, angle, label in zip(self.axes, self.angles, labels):
			ax.set_rgrids(range(1, self.n+1), angle=angle, labels=label)
			ax.spines["polar"].set_visible(False)
			ax.set_ylim(0, 5)

	def plot(self, values, *args, **kw):
		angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
		values = np.r_[values, values[0]]
		self.ax.plot(angle, values, *args, **kw)

class RadarMDI(myMDI):
	def setup(self):
		fig = plt.figure(figsize=(6, 6))
		titles=self.model.inputNames+self.model.outputNames
		labels = [["0.2","0.4","0.6","0.8","1"]]*len(self.model.inputNames+self.model.outputNames)
		radar = Radar(fig, titles, labels)
		radar.plot([5*abs(x) for x in self.model.corrmat[self.var1,:]],  "-", lw=2, color="b", alpha=0.4, label=self.model.getVariableIndex(self.var1))
		self.canvas = FigureCanvas(fig)
		#wd=QtGui.QWidget()
		self.setWidget(self.canvas)
		self.setWindowTitle("Correlation Radar Plot " +str(self.model.getIndexVariable(self.var1)))


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
		self.setWindowTitle("Statistical Data")

class scattMDI(myMDI):

	def setup(self):
		self.roi = pg.RectROI([0,0],[1,1],pen=pg.mkPen('r'))
		pw = subScatter(self, self.model, [self.var1, self.var2], self.roi)
		self.center = QtGui.QWidget()
		self.center.verticalLayout = QtGui.QVBoxLayout(self.center)


		t = self.model.data[:, self.var1]
		s = self.model.data[:, self.var2]
		self.model.subscribeSelection(self)
		def changed(old, new):
			if (int(new) == 10 and int(old) == 8):
				self.overlay.show()
			if (int(new) == 8 and int(old) == 10):
				self.overlay.hide()




		self.windowStateChanged.connect(changed)

		pw.addItem(self.roi)
		pw.sigRangeChanged.connect(self.rangeChanged)


		self.roi.setZValue(10)
		pw.x = t
		pw.y = s
		self.roi.hide()
		
		self.setWindowTitle("ScatterPlot: "+str(self.model.getIndexVariable(self.var1))+ " / " +str(self.model.getIndexVariable(self.var2)))

		self.s2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen('k'), pxMode=True)
		self.s3 = pg.ScatterPlotItem(size=10, pen=pg.mkPen('k'), pxMode=True)
		self.refresh()

		self.overlay = pg.PlotWidget(pw)
		self.overlay.addItem(self.s3)
		vb = self.overlay.getPlotItem().getViewBox()
		roisize = [max(t)-min(t), max(s)-min(s)]
		self.overroi = pg.RectROI([min(t),min(s)],roisize, pen=pg.mkPen('r'), movable=False)
		self.overlay.addItem(self.overroi)
		for handle in self.overroi.getHandles():
			self.overroi.removeHandle(handle)
		self.overroi.show()
		viewrange = vb.viewRange()
		rangex = viewrange[0]
		rangey = viewrange[1]
		width = (rangex[1] - rangex[0])
		height = (rangey[1] - rangey[0])
		width = max(t)-min(t)
		height = max(s)-min(s)
		self.overlay.setFixedSize(200,150)
		self.overlay.move(50 , 25)
		self.overlay.hideButtons()
		self.overlay.setMouseEnabled(False, False)
		self.overlay.setBackground(0.89)
		self.overlay.hide()

		pw.addItem(self.s2)
		self.center.verticalLayout.addWidget(pw)
		self.setWidget(self.center)

	def refresh(self):
		self.s2.clear()
		self.s3.clear()
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
				size = 2
			spots.append({'pos': [t[i],s[i]], 'data': 1, 'symbol': 'o', 'size': size, 'pen': pen})
		self.s2.addPoints(spots)
		self.s3.addPoints(spots)
	def rangeChanged(self, scatter, ranges):
		rangex = ranges[0]
		rangey = ranges[1]
		self.overroi.setPos([rangex[0],rangey[0]])
		self.overroi.setSize([rangex[1]-rangex[0], rangey[1]-rangey[0]])


def correlationColor(corr):
	summer = plt.get_cmap(scheme)
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
