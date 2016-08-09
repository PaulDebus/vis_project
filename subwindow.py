import pyqtgraph as pg
import matplotlib.pyplot
from pyqtgraph.Qt import QtGui
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


class scattMDI(myMDI):

	def setup(self):
		#corr = self.model.corrmat[self.var1, self.var2]
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
		self.setWindowTitle("ScatterPlot: "+str(self.model.getIndexVariable(self.var1))+ " / " +str(self.model.getIndexVariable(self.var2)))


def correlationColor(corr):
	summer = matplotlib.pyplot.get_cmap(scheme)
	return tuple([255*i for i in list(summer(abs(corr)))])
