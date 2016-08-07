from PyQt4.uic import loadUiType
from PyQt4.uic import loadUi
from pyqtgraph.Qt import QtGui
import plots


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
			# if widget has some id attributes you need to
			# save in a list to maintain order, you can do that here
			# i.e.:   aList.append(widget.someId)
			widget.deleteLater()
		size = self.variableList.frameGeometry(
			).width() / len(self.model.activeVariables)
		num = len(model.activeVariables)
		print(model.activeVariables)
		for row in range(1, num+1):
			for col in range(row, num+1):
				var1 = model.getVariableIndex(model.activeVariables[row-1])
				var2 = model.getVariableIndex(model.activeVariables[col-1])
				if row == col:
					plot = plots.histogram(self.model, variables=var1, parent=None, width=size, height=size)
				else:
					plot = plots.scatterplot(self.model, variables=[var1, var2],
											parent=None, width=size, height=size)
				self.matrixWindow.gridLayout.addWidget(plot,num+1-row,col)
		size = self.splitter.size().width()
		self.splitter.setSizes([200, size-200])
		self.resizeLeft()
		
		while self.matrixWindow.horizontalLayout_2.count():
			item = self.matrixWindow.horizontalLayout_2.takeAt(0)
			widget = item.widget()
			widget.deleteLater()
			item = self.matrixWindow.verticalLayout_3.takeAt(0)
			widget = item.widget()
			widget.deleteLater()

		for name in model.activeVariables:
			label1 = QtGui.QLabel(name)
			label2 = QtGui.QLabel(name)
			self.matrixWindow.horizontalLayout_2.addWidget(label1)
			self.matrixWindow.verticalLayout_3.addWidget(label2)

	def loadNames(self):
		qmodel = QtGui.QStandardItemModel(self.variableList)
		qmodel.itemChanged.connect(self.listChange)
		# QObject.connect(qmodel,SIGNAL('selectionChanged()',listChange))
		variables = self.model.inputNames + self.model.outputNames
		for var in variables:
			item = QtGui.QStandardItem(var)
			item.setCheckable(True)
			if var in self.model.activeVariables:
				item.setCheckState(2)
			qmodel.appendRow(item)
		self.variableList.setModel(qmodel)

	def listChange(self,e):
		print(e.text(),e.checkState())
		if e.checkState()==0:
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
