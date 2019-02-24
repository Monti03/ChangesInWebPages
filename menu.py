from PyQt4              import QtGui, QtCore

running_threads = []

class Menu(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle('Threads')
        self.resize(400, 100)
        self.setWindowIcon(QtGui.QIcon('media/logo.png'))

        cWidget = QtGui.QWidget(self)

        grid = QtGui.QGridLayout(cWidget)

        url = QtGui.QLabel("urls",cWidget)
        time = QtGui.QLabel("mins", cWidget)
        last = QtGui.QLabel("last check", cWidget)

        grid.addWidget(url,     0, 0)
        grid.addWidget(time,    0, 1)
        grid.addWidget(last,    0, 2)


        ths = running_threads
        #print("menu->"+str(ths))
        i = 1
        for t in ths:
            t.update_gui.connect(self._update_gui)

            url = QtGui.QLabel(t._url, cWidget)
            time = QtGui.QLabel(str(t._mins), cWidget)
            last = QtGui.QLabel(str(t._last_check), cWidget)

            grid.addWidget(url,     i, 0)
            grid.addWidget(time,    i, 1)
            grid.addWidget(last,    i, 2)

            i+=1
        
        cWidget.setLayout(grid)
        self.setCentralWidget(cWidget)
    
    def _update_gui(self):
        print("Update Menu Gui")
        cWidget = QtGui.QWidget(self)

        new_grid = QtGui.QGridLayout(cWidget)

        url = QtGui.QLabel("urls", cWidget)
        time = QtGui.QLabel("mins", cWidget)
        last = QtGui.QLabel("last check", cWidget)

        new_grid.addWidget(url,     0, 0)
        new_grid.addWidget(time,    0, 1)
        new_grid.addWidget(last,    0, 2)

        i = 1
        for t in running_threads:
            url = QtGui.QLabel(t._url, cWidget)
            time = QtGui.QLabel(str(t._mins), cWidget)
            last = QtGui.QLabel(str(t._last_check), cWidget)

            new_grid.addWidget(url,     i, 0)
            new_grid.addWidget(time,    i, 1)
            new_grid.addWidget(last,    i, 2)

            i   += 1

        cWidget.setLayout(new_grid)
        self.setCentralWidget(cWidget)
        
            

        