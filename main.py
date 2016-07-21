from PyQt4.uic import loadUiType
from PyQt4.uic import loadUi
from PyQt4.QtGui import *
import plots


Ui_MainWindow, QMainWindow = loadUiType('GUI/MainWindow.ui')

class Main(QMainWindow, Ui_MainWindow):

	def __init__(self, model):
		self.model=model
		super(Main, self).__init__()
		self.setupUi(self)
		self.splitter.splitterMoved.connect(self.resizeLeft)
		loadUi('GUI/mat.ui', self.matrixWindow)

	def addMatrix(self):
		size = self.variableList.frameGeometry().width() / len(self.model.activeVariables)
		num = len(model.activeVariables)
		for row in range(1,num+1):
			for col in range(row,num+1):
				if row == col:
					plot = plots.histogram(self.model, variables = row,
						parent=None, width = size, height= size)
				else:
					plot = plots.scatterplot(self.model, variables = [row+2,col+2],
						parent=None, width = size, height= size)
				self.matrixWindow.gridLayout.addWidget(plot,num+1-row,col)
		size = self.splitter.size().width()
		self.splitter.setSizes([200, size-200])
		self.resizeLeft()

	def loadNames(self):
		qmodel = QStandardItemModel(self.variableList)
		qmodel.itemChanged.connect(self.listChange)
		#QObject.connect(qmodel,SIGNAL('selectionChanged()',listChange))
		variables = self.model.inputNames + self.model.outputNames
		for var in variables:
			item = QStandardItem(var)
			item.setCheckable(True)
			if var in self.model.activeVariables:
				item.setCheckState(2)
			qmodel.appendRow(item)
		self.variableList.setModel(qmodel)

	def listChange(self,e):
		print(e.text(),e.checkState())
		if e.checkState==0:
			self.model.setPassiveVar(e.text())
		else:
			self.model.setActiveVar(e.text())
		self.addMatrix()
	
	def resizeLeft(self):
		size = self.variableList.frameGeometry().width()
		self.matrixWindow.resize(size,size)

if __name__ == '__main__':
	import sys
	from PyQt4 import QtGui
	import model

	model = model.fromFile('output.txt')
	app = QtGui.QApplication(sys.argv)
	main = Main(model)
	main.addMatrix()
	main.loadNames()
	main.show()
	sys.exit(app.exec_())
