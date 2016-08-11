import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
from scipy import stats as st
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from scipy import stats

scheme='summer'

class myMDI(QtGui.QMdiSubWindow):
	def __init__(self, model, var1, var2):
		super(QtGui.QMdiSubWindow, self).__init__()
		self.model = model
		self.var1 = var1
		self.var2 = var2
		self.setup()
		self.windowStateChanged.connect(self.changed)

	def changed(self, old, new):
		pass

class histMDI(myMDI):
	#simple histogram
	def setup(self):
		pg.setConfigOption('foreground', 'k')
		self.center = QtGui.QWidget()
		self.lay = QtGui.QVBoxLayout(self.center)
		self.pw = pg.PlotWidget()
		d = self.model.data[:, self.var1]
		y,x = np.histogram(d, bins=25)
		color = correlationColor(0.5)
		self.pw.plot(x,y, stepMode=True, fillLevel=0, pen='k', brush=color)
		self.lay.addWidget(self.pw)

		self.txt = QtGui.QLabel()
		self.fitDist(max(y))
		self.txt.hide()
		self.lay.addWidget(self.txt)

		self.setWidget(self.center)
		self.setWindowTitle("Histogramm: "+str(self.model.getIndexVariable(self.var1)))

	def changed(self,old, new):
		if (int(new) == 10 and int(old) == 8):
			self.txt.show()
			self.dist.show()
			self.lay.addWidget(self.txt)
		if (int(new) == 8 and int(old) == 10):
			self.txt.hide()
			self.dist.hide()
			self.lay.removeWidget(self.txt)
	
	def fitDist(self, height):
		rvs = self.model.data[:, self.var1]
		sm = rvs.mean()
		sstd = np.sqrt(rvs.var())
		ssupp = (rvs.min(), rvs.max())
		pval = 0
		stat = None
		name = None
		params = None
		distrib = None
		for distr in [stats.norm, stats.chi2, stats.lognorm, stats.expon, stats.frechet_r, stats.frechet_l, stats.lognorm, stats.uniform, stats.wald]:
			distname = distr.name
			# estimate parameters
			par_est = distr.fit(rvs,loc=sm, scale=sstd)
			arg_est = par_est[:-2]	# get scale parameters if any
			loc_est = par_est[-2]
			scale_est = par_est[-1]
			rvs_normed = (rvs-loc_est)/scale_est
			ks_stat, ks_pval = stats.kstest(rvs_normed,distname, arg_est)
			if ks_pval > pval:
				pval = ks_pval
				stat = ks_stat
				name = distname
				params = par_est
				distrib = distr

		table = """<table>
			<th> Best fitting distribution: {name} </th>
			<tr> <td> P Value: </td> <td> {pval} </td></tr>
			<tr> <td> Mean: </td> <td> {mean} </td></tr>
			<tr> <td> Standard Deviation: </td> <td> {std} </td></tr>
			<tr> <td> Shape Parameters: </td> <td> {params} </td></tr>
		</table>"""
		self.txt.setText(table.format(name=name, pval = pval, mean = params[-2], std = params[-1], params = params))

		xvals = np.linspace(ssupp[0],ssupp[1],100)
		yvals = distrib.pdf(xvals, loc=params[-2], scale=params[-1], *params[:-2])
		maxy = yvals.max()
		yvals = yvals/maxy*height
		self.dist = pg.PlotCurveItem(xvals, yvals, pen =pg.mkPen('r', width=2) )
		self.pw.getPlotItem().addItem(self.dist)
		self.dist.hide()

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
	#radar plot giving a convinient way of seeing correlations of one parameter to all others
	def setup(self):
		fig = plt.figure(figsize=(6, 6))
		titles=self.model.inputNames+self.model.outputNames
		labels = [["0.2","0.4","0.6","0.8","1"]]*len(self.model.inputNames+self.model.outputNames)
		radar = Radar(fig, titles, labels)
		lColor=tuple([1/255*i for i in list(correlationColor(0))])
		radar.plot([5*abs(x) for x in self.model.corrmat[self.var1,:]],	"-", lw=2, color=lColor, alpha=0.4, label=self.model.getVariableIndex(self.var1))
		self.canvas = FigureCanvas(fig)
		#wd=QtGui.QWidget()
		self.setWidget(self.canvas)
		self.setWindowTitle("Correlation Radar Plot " +str(self.model.getIndexVariable(self.var1)))


class MeanStdMDI(myMDI):
	#stacked graph showing simple statistical parameters
	def setup(self):
		pw = pg.PlotWidget()
		#num of steps
		bin=20
		#get aata
		t = self.model.data[:, self.var1]
		s = self.model.data[:, self.var2]
		#generate 'histogram' with mean values, std and edges 
		mean,edges,c=st.binned_statistic(t,s,statistic='mean',bins=bin)
		max,edges,c=st.binned_statistic(t,s,statistic=np.amax,bins=bin)
		min,edges,c=st.binned_statistic(t,s,statistic=np.amin,bins=bin)
		std,edges,c=st.binned_statistic(t,s,statistic=np.std,bins=bin)
		#creates upper and lower bound
		stdMin=[]
		stdMax=[]
		for i in range(0,len(mean)):
			stdMin.append(mean[i]-std[i])
			stdMax.append(mean[i]+std[i])
		#transfer edges to midpoints
		midpoints=[]
		old=edges[0]
		for i in edges:
			midpoints.append((old+i)/2)
			old=i
		midpoints.pop(0)
		#generate fill and fillcolor
		colorMinMax=correlationColor(0.66)
		colorMinMax=tuple([colorMinMax[0],colorMinMax[1],colorMinMax[2],150])
		colorStd=correlationColor(0.33)
		colorStd=tuple([colorStd[0],colorStd[1],colorStd[2],150])
		#plot lines
		minPlot=pg.PlotDataItem(midpoints, min, pen=pg.mkPen(colorMinMax,width=2), name='MinValue')
		stdMinPlot=pg.PlotDataItem(midpoints, stdMin, pen=pg.mkPen(colorStd,width=2), name='MinStd')
		meanPlot=pg.PlotDataItem(midpoints, mean, pen=pg.mkPen('k',width=2), name='MeanValue')
		stdMaxPlot=pg.PlotDataItem(midpoints, stdMax, pen=pg.mkPen(colorStd,width=2), name='maxStd')
		maxPlot=pg.PlotDataItem(midpoints, max, pen=pg.mkPen(colorMinMax,width=2),name='MaxValue')
		fill1=pg.FillBetweenItem(minPlot, maxPlot, brush=pg.mkBrush(colorMinMax))
		fill2=pg.FillBetweenItem(stdMinPlot, stdMaxPlot, brush=pg.mkBrush(colorStd))
		#add all to graph
		pw.addLegend()
		pw.addItem(minPlot)
		pw.addItem(stdMinPlot)
		pw.addItem(meanPlot)
		pw.addItem(stdMaxPlot)
		pw.addItem(maxPlot)
		pw.addItem(fill1)
		pw.addItem(fill2)
		self.setWidget(pw)
		self.setWindowTitle("Mean- and StandardDeviationPlot: "+str(self.model.getIndexVariable(self.var1))+ " / " +str(self.model.getIndexVariable(self.var2)))

class TextMDI(myMDI):
	#simple textwidget givin relevant informations about given parameters
	def setup(self):
		self.model.subscribeSelection(self)
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
		title=QtGui.QLabel("<h2>Statistical Data from: </h2>")
		table1=QtGui.QLabel(table1)
		hbox=QtGui.QHBoxLayout()
		hbox.addWidget(QtGui.QLabel(table2))
		hbox.addWidget(QtGui.QLabel(table3))
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(title)
		vbox.addWidget(table1)
		vbox.addItem(hbox)
		tWidget=QtGui.QWidget()
		self.pointTable=QtGui.QTableWidget(parent=tWidget)
		self.pointTable.hide()
		self.refresh()
		vbox.addWidget(self.pointTable)
		pw.setLayout(vbox)
		self.setWidget(pw)
		self.setWindowTitle("Statistical Data: " +self.model.getIndexVariable(self.var1) + " / " + self.model.getIndexVariable(self.var2))
	
	def refresh(self):
	#adds table with data of selected points
		selection = self.model.selection
		if len(selection)==0:
			self.pointTable.hide()
		else:
			headers = self.model.inputNames+self.model.outputNames
			col=len(headers)
			row=len(selection)
			self.pointTable.setColumnCount(col)
			self.pointTable.setRowCount(row)
			self.pointTable.setHorizontalHeaderLabels(headers)
			for n in range(0,col):
				for m in range(0,row):
					newitem = QtGui.QTableWidgetItem(str(self.model.data[selection[m],n]))
					print(newitem)
					self.pointTable.setItem(m, n, newitem)
			self.pointTable.show()


class scattMDI(myMDI):
	#scatterplot of both varibles including brushing and linking as well as overview map
	def changed(self,old, new):
		if (int(new) == 10 and int(old) == 8):
			self.overlay.show()
		if (int(new) == 8 and int(old) == 10):
			self.overlay.hide()

	def setup(self):
		self.roi = pg.RectROI([0,0],[1,1],pen=pg.mkPen('r'))
		pw = subScatter(self, self.model, [self.var1, self.var2], self.roi)
		self.center = QtGui.QWidget()
		self.center.verticalLayout = QtGui.QVBoxLayout(self.center)
		t = self.model.data[:, self.var1]
		s = self.model.data[:, self.var2]
		self.model.subscribeSelection(self)
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

class varMDI(myMDI):
	def setup(self):
		w = pg.PlotWidget()
		vars = [abs(i) for i in self.model.cop[:,self.var1-len(self.model.inputNames)]]
		label = self.model.inputNames
		labels = []
		data = []
		for i in range(len(label)):
			if vars[i] > 0.05:
				data.append(vars[i])
				labels.append(label[i])

		color = [tuple([j/255 for j in list(correlationColor(i))]) for i in data]

		fig = plt.figure(figsize=(6,6))
		plt.pie(data, labels=labels, colors=color, autopct='%1.1f%%', shadow=False, startangle=90)
		plt.axis('equal')
		self.canvas = FigureCanvas(fig)
		self.setWidget(self.canvas)


#		set_angle = 0
#		for i in range(len(vars)):
#			label = self.model.inputNames[i]
#			angle= vars[i]
#			ellipse = QtGui.QGraphicsEllipseItem(0,0,400,400)
#			ellipse.setPos(200,200)
#			ellipse.setStartAngle(set_angle)
#			ellipse.setSpanAngle(angle)
#			set_angle += angle
#			w.getPlotItem().addItem(ellipse)
