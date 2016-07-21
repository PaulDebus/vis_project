from PyQt4.uic import loadUiType
from PyQt4.uic import loadUi
from PyQt4.QtGui import *
import plots

import matplotlib.pyplot as plt



Ui_MainWindow, QMainWindow = loadUiType('GUI/MainWindow.ui')


class Main(QMainWindow, Ui_MainWindow):

    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)

    def addMatrix(self, model):
        loadUi('GUI/Matrix.ui', self.matrixWindow)
        size = self.variableList.frameGeometry().width() / len(model.activeVariables)
        self.splitter.splitterMoved.connect(self.resizeLeft)
        num = len(model.activeVariables)
        for row in range(1,num+1):
            for col in range(row,num+1):
                if row == col:
                    plot = plots.histogram(model, variables = row,
                        parent=None, width = size, height= size)
                else:
                    plot = plots.scatterplot(model, variables = [row+2,col+2],
                        parent=None, width = size, height= size)
                self.matrixWindow.gridLayout.addWidget(plot,num+1-row,col)

    def loadNames(self, model):
        qmodel = QStandardItemModel(self.variableList)
        variables = model.inputNames + model.outputNames
        for var in variables:
            item = QStandardItem(var)
            item.setCheckable(True)
            item.setCheckState(True)
            qmodel.appendRow(item)
        self.variableList.setModel(qmodel)

    def resizeLeft(self):
        size = self.variableList.frameGeometry().width()
#        self.matrixWindow.widget.setGeometry(

if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    import model

    model = model.fromFile('output.txt')
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.addMatrix(model)
    main.loadNames(model)
    main.show()
    sys.exit(app.exec_())
