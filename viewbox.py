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