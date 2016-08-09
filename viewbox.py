import pyqtgraph as pg
from pyqtgraph.Point import Point
from pyqtgraph.Qt import QtCore
#TODO Löschen?

class MyViewBox(pg.ViewBox):

    def mouseDragEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            ev.ignore()
        else:
            pg.ViewBox.mouseDragEvent(self, ev)
    '''

        pos = ev.pos()
        if ev.button() == QtCore.Qt.RightButton:
            print('right')
            if ev.isFinish():
                self.rbScaleBox.hide()
                #self.ax = QtCore.QRectF(Point(ev.buttonDownPos(ev.button())), Point(pos))
                #self.ax = self.childGroup.mapRectFromParent(self.ax)
                #self.Coords =  self.ax.getCoords()
            else:
                self.updateScaleBox(ev.buttonDownPos(), ev.pos())
                '''
