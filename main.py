from PyQt4.uic import loadUiType
from PyQt4.uic import loadUi
from PyQt4.QtGui import *


Ui_MainWindow, QMainWindow = loadUiType('GUI/MainWindow.ui')


class Main(QMainWindow, Ui_MainWindow):

    def __init__(self, ):
        super(Main, self).__init__()
        self.setupUi(self)

    def addMatrix(self):
        loadUi('GUI/Matrix.ui', self.matrixWindow)

    def loadNames(self, model):
        qmodel = QStandardItemModel(self.variableList)
        variables = model.inputNames + model.outputNames
        for var in variables:
            item = QStandardItem(var)
            item.setCheckable(True)
            qmodel.appendRow(item)
        self.variableList.setModel(qmodel)


if __name__ == '__main__':
    import sys
    from PyQt4 import QtGui
    import model

    model = model.fromFile('output.txt')
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.addMatrix()
    main.loadNames(model)
    main.show()
    sys.exit(app.exec_())
