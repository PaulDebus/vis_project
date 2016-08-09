from PyQt4.uic import loadUiType
from PyQt4.uic import loadUi
from pyqtgraph.Qt import QtGui, QtCore
import plots
import subwindow


Ui_MainWindow, QMainWindow = loadUiType('GUI/MainWindow.ui')


class Main(QMainWindow, Ui_MainWindow):

	def __init__(self, model):
		self.model = model
		super(Main, self).__init__()
		self.setupUi(self)
		self.splitter.splitterMoved.connect(self.resizeLeft)
		loadUi('GUI/mat.ui', self.matrixWindow)


	def addMatrix(self):
		while self.matrixWindow.gridLayout.count():
				item = self.matrixWindow.gridLayout.takeAt(0)
				widget = item.widget()
				widget.deleteLater()
		size = self.variableList.frameGeometry().width() / len(self.model.activeVariables)
		num = len(model.activeVariables)
		if num > 3:
			colorBar= plots.colorBar(self.model,parent=self, width=size, height=size)
			self.matrixWindow.gridLayout.addWidget(colorBar,1,1,2,2)
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
		qmodel = QtGui.QStandardItemModel(self.variableList)
		qmodel.itemChanged.connect(self.listChange)
		variables = self.model.inputNames + self.model.outputNames
		for var in variables:
			item = QtGui.QStandardItem(var)
			item.setCheckable(True)
			if var in self.model.activeVariables:
				item.setCheckState(2)
			qmodel.appendRow(item)
		self.variableList.setModel(qmodel)

	def listChange(self,e):
		if e.checkState()==0:
			self.model.setPassiveVar(e.text())
		else:
			self.model.setActiveVar(e.text())
		print(e.text(),e.checkState(),self.model.getVariableIndex(e.text()))
		self.addMatrix()

	def resizeLeft(self):
		size = self.variableList.frameGeometry().width()
		self.matrixWindow.resize(size, size)


	def showDataBoxes(self):
		mdi = self.mdiArea
		mdi.closeAllSubWindows()
		index1, index2 = self.model.getSelectedVariables()
		var1 = self.model.getIndexVariable(index1)
		var2 = self.model.getIndexVariable(index2)
		self.label.setText("{0}, {1}".format(var1, var2))

		subs = []
		subs.append(subwindow.histMDI(self.model, index1, index2))
		subs.append(subwindow.scattMDI(self.model, index1, index2))
		subs.append(subwindow.scattMDI(self.model, index1, index2))
		subs.append(subwindow.histMDI(self.model, index2, index1))
		subs.append(subwindow.MeanStdMDI(self.model, index1, index2))
		for sub in subs:
			mdi.addSubWindow(sub)
			sub.show()
		mdi.tileSubWindows()


if __name__ == '__main__':
	import sys
	from PyQt4 import QtGui
	import model

	model = model.fromFile('output.txt')
	app = QtGui.QApplication(sys.argv)
	main = Main(model)
	main.addMatrix()
	main.loadNames()
	main.showDataBoxes()
	main.show()
	sys.exit(app.exec_())
