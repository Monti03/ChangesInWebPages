from PyQt4              import QtGui, QtCore


class Menu(QtGui.QMainWindow):
    def __init__(self, gui):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle('Threads')
        self.resize(400, 100)
        self.setWindowIcon(QtGui.QIcon('media/logo.png'))

        self._cWidget = QtGui.QWidget(self)

        grid = QtGui.QGridLayout(self._cWidget)

        url = QtGui.QLabel("urls", self._cWidget)
        time = QtGui.QLabel("mins", self._cWidget)
        last = QtGui.QLabel("last check", self._cWidget)

        grid.addWidget(url,     0, 0)
        grid.addWidget(time,    0, 1)
        grid.addWidget(last,    0, 2)


        ths = gui._running_threads
        print(ths)
        i = 1
        for t in ths:
            url = QtGui.QLabel(t._url, self._cWidget)
            time = QtGui.QLabel(str(t._mins), self._cWidget)
            last = QtGui.QLabel(str(t._last_check), self._cWidget)

            grid.addWidget(url,     i, 0)
            grid.addWidget(time,    i, 1)
            grid.addWidget(last,    i, 2)
            

            i+=1
        
        self._cWidget.setLayout(grid)
        self.setCentralWidget(self._cWidget)

        