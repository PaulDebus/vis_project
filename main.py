'''Usage: main.py <file>
'''
from PyQt4.uic import loadUiType
from docopt import docopt
from PyQt4.uic import loadUi
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import plots
import subwindow
import numpy as np
import pyqtgraph.exporters
import os.path
import math


Ui_MainWindow, QMainWindow = loadUiType('GUI/MainWindow.ui')


class Main(QMainWindow, Ui_MainWindow):

	def __init__(self, model):
		self.model = model
		super(Main, self).__init__()
		self.setupUi(self)
		self.splitter.splitterMoved.connect(self.resizeLeft)
		loadUi('GUI/mat.ui', self.matrixWindow)
		bar = self.menuBar()
		#creates emnubar in main menu
		subWindowMenu = bar.addMenu("New Subwindow")
		exportMenu = bar.addMenu("Export")
		subWindowMenu.addAction("Scatter Plot")
		subWindowMenu.addAction("Histogram 1")
		subWindowMenu.addAction("Histogram 2")
		subWindowMenu.addAction("Mean + Std")
		subWindowMenu.addAction("Statistics")
		subWindowMenu.addAction("Radar 1")
		subWindowMenu.addAction("Radar 2")
		subWindowMenu.addAction("Var Pie 1")
		subWindowMenu.addAction("Var Pie 2")
		exportMenu.addAction("Export selected subwindow as JPG")
		subWindowMenu.triggered[QtGui.QAction].connect(self.windowAction)
		exportMenu.triggered[QtGui.QAction].connect(self.exportAction)

	def windowAction(self,q):
		#usuability of menubar
		index1, index2 = self.model.getSelectedVariables()
		if q.text() == "Scatter Plot":
			sub = subwindow.scattMDI(self.model, index1, index2)
		if q.text() == "Histogram 1":
			sub = subwindow.histMDI(self.model, index1, index2)
		if q.text() == "Histogram 2":
			sub = subwindow.histMDI(self.model, index2, index2)
		if q.text() == "Mean + Std":
			sub = subwindow.MeanStdMDI(model, index1, index2)
		if q.text() == "Statistics":
			sub = subwindow.TextMDI(model, index1, index2)
		if q.text() == "Radar 1":
			sub = subwindow.RadarMDI(model, index1, index2)
		if q.text() == "Radar 2":
			sub = subwindow.RadarMDI(model, index2, index1)
		if q.text() == "Var Pie 1":
			sub = subwindow.varMDI(self.model, index1, index2)
		if q.text() == "Var Pie 2":
			sub = subwindow.varMDI(self.model, index2, index1)
		self.mdiArea.addSubWindow(sub)
		sub.show()
		self.mdiArea.tileSubWindows()
		
	def exportAction(self,q):
		#usuability of menubar
		if q.text() == "Export selected subwindow as JPG":
			widget=self.mdiArea.activeSubWindow().widget()
			title=self.mdiArea.activeSubWindow().windowTitle()
			p=QtGui.QPixmap.grabWindow(widget.winId())
			path = os.path.abspath(__file__)
			directory="Exported_Images"
			if not os.path.exists(directory):
				os.makedirs(directory)
			title=title.replace('/','')
			title=title.replace(':','')
			title=title.replace('	 ','_')
			title=title.replace('	','_')
			title=title.replace(' ','_')
			title='Exported_Images/' + title+ '.jpg'
			p.save(title, 'jpg')



	def addMatrix(self):
	#creates "menu"-Matrix window 
		while self.matrixWindow.gridLayout.count():
				item = self.matrixWindow.gridLayout.takeAt(0)
				widget = item.widget()
				widget.deleteLater()
		size = self.variableList.frameGeometry().width() / len(self.model.activeVariables)
		num = len(model.activeVariables)
		colorBar=plots.colorBar(2*size,6*size)
		if num > 3:
			self.matrixWindow.gridLayout.addWidget(colorBar, 1,1,math.ceil(num/2)-1,math.ceil(num/2)-1)
		for row in range(1, num+1):
			for col in range(row, num+1):
				var1 = model.getVariableIndex(model.activeVariables[row-1])
				var2 = model.getVariableIndex(model.activeVariables[col-1])
				if row == col:
					plot = plots.histogram(self.model, variables=var1, parent=None, width=size, height=size)
				else:
					plot = plots.scatterplot(self.model, variables=[var1, var2],parent=self, width=size, height=size)
				self.matrixWindow.gridLayout.addWidget(plot,num+1-row,col)
			label = QtGui.QLabel(model.activeVariables[row-1])
			self.matrixWindow.gridLayout.addWidget(label,num+1-row,num+1)
		for name in model.activeVariables:
			label = QtGui.QLabel(name)
			self.matrixWindow.gridLayout.addWidget(label,num+1,model.activeVariables.index(name)+1)
		size = self.splitter.size().width()
		self.resizeLeft()

	def loadNames(self):
	#creates checkitems for different parameters
		qmodel = QtGui.QStandardItemModel(self.variableList)
		qmodel.itemChanged.connect(self.listChange)
		variables = self.model.inputNames + self.model.outputNames
		it = QtGui.QStandardItem("Input Variables")
		it.setCheckable(False)
		it.setBackground(QtGui.QColor('lightGray'))
		f = it.font()
		f.setBold(True)
		it.setFont(f)
		qmodel.appendRow(it)
		for var in self.model.inputNames:
			item = QtGui.QStandardItem(var)
			item.setCheckable(True)
			if var in self.model.activeVariables:
				item.setCheckState(2)
				item.setBackground(QtGui.QColor('lightGray'))
			qmodel.appendRow(item)
		it = QtGui.QStandardItem("Output Variables")
		it.setCheckable(False)
		f = it.font()
		f.setBold(True)
		it.setFont(f)
		qmodel.appendRow(it)
		for var in self.model.outputNames:
			item = QtGui.QStandardItem(var)
			item.setCheckable(True)
			if var in self.model.activeVariables:
				item.setCheckState(2)
			qmodel.appendRow(item)
		self.variableList.setModel(qmodel)

	def listChange(self,e):
	#listener for checklist
		if e.checkState()==0:
			self.model.setPassiveVar(e.text())
		else:
			self.model.setActiveVar(e.text())
		self.addMatrix()

	def resizeLeft(self):
	#fits matrixWindow when splitter resizes
		size = self.variableList.frameGeometry().width()
		self.matrixWindow.resize(size, size)


	def showDataBoxes(self, new=True):
	#creates subwindows for selected variablepair
		mdi = self.mdiArea
		mdi.closeAllSubWindows()
		index1, index2 = self.model.getSelectedVariables()
		var1 = self.model.getIndexVariable(index1)
		var2 = self.model.getIndexVariable(index2)
		self.label.setText("{0}, {1}".format(var1, var2))

		subs = []
		subs.append(subwindow.histMDI(self.model, index1, index2))
		subs.append(subwindow.scattMDI(self.model, index1, index2))
		subs.append(subwindow.histMDI(self.model, index2, index1))
		if abs(self.model.corrmat[index1, index2])>0.25:
			subs.append(subwindow.MeanStdMDI(self.model, index1, index2))
		if len(np.where(abs(self.model.corrmat[:, index1])>0.2)[0])>2:
			subs.append(subwindow.RadarMDI(self.model, index1, index2))
		if self.model.getIndexVariable(index1) in self.model.outputNames:
			subs.append(subwindow.varMDI(self.model, index1, index2))
		subs.append(subwindow.TextMDI(self.model, index1, index2))
		for sub in subs:
			mdi.addSubWindow(sub)
			sub.show()
		mdi.tileSubWindows()


if __name__ == '__main__':
	import sys
	from PyQt4 import QtGui
	import model

	opts = docopt(__doc__)

	if not os.path.exists(opts['<file>']):
			import writeValues
			name = opts['<file>'].split('.')[0]
			writeValues.write(opts['<file>'])
	model = model.fromFile(opts['<file>'])
	app = QtGui.QApplication(sys.argv)
	main = Main(model)
	main.addMatrix()
	main.loadNames()
	main.showDataBoxes()
	main.show()
	sys.exit(app.exec_())
