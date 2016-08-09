import numpy as np
import pyqtgraph as pg
import colorBar
import matplotlib.pyplot

if __name__ == '__main__':
    app = pg.mkQApp()

    summer = matplotlib.pyplot.get_cmap('summer')
    # use less ink
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

    pw = pg.plot()
    
    # make colormap
    stops = np.r_[-1.0, -0.5, 0.5, 1.0]
    colors = np.array([summer(i) for i in stops])
    cm = pg.ColorMap(stops, colors)
    
    # make colorbar, placing by hand
    cb = colorBar.ColorBar(cm, 10, 200, label='Foo (Hz)')#, [0., 0.5, 1.0])
    pw.scene().addItem(cb)
    cb.translate(570.0, 90.0)

    app.exec_()