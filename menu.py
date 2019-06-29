from PyQt5              import QtGui, QtCore, QtWidgets

running_threads = []
class Menu(QtWidgets.QMainWindow):
    def __init__(self, gui):
        QtWidgets.QMainWindow.__init__(self)

        self.setWindowTitle('Threads')
        self.resize(400, 100)
        self.setWindowIcon(QtGui.QIcon('media/logo.png'))
        
        #on this object will arrive notification from main gui
        gui.main_gui_notification_to_menu.connect(self._update_gui)

        cWidget = QtWidgets.QWidget(self)

        grid = QtWidgets.QGridLayout(cWidget)

        #labels
        url = QtWidgets.QLabel("urls",cWidget)
        time = QtWidgets.QLabel("mins", cWidget)
        last = QtWidgets.QLabel("last check", cWidget)

        #adding labels to the grid
        grid.addWidget(url,     0, 0)
        grid.addWidget(time,    0, 1)
        grid.addWidget(last,    0, 2)

        #fill grid with threads values
        i = 1
        for tpl in running_threads:
            t = tpl[0]
            if(not tpl[1]):
                t.update_gui.connect(self._update_gui)
                tpl[1] = True

            url = QtWidgets.QLabel(t._url, cWidget)
            time = QtWidgets.QLabel(str(t._mins), cWidget)
            last = QtWidgets.QLabel(str(t._last_check), cWidget)

            button = QtWidgets.QPushButton("STOP", self)
            button.clicked.connect(self._make_pressed(t))

            grid.addWidget(url,     i, 0)
            grid.addWidget(time,    i, 1)
            grid.addWidget(last,    i, 2)
            grid.addWidget(button,  i, 3)

            i+=1
        
        cWidget.setLayout(grid)
        self.setCentralWidget(cWidget)
    
    #this function returns a function that associate button and thread
    def _make_pressed(self, t):
        def pressed():
            t.stop()
        return pressed

    #update of the menu gui -> new thread or new last_check
    def _update_gui(self):
        print("Update Menu Gui")
        cWidget = QtWidgets.QWidget(self)

        new_grid = QtWidgets.QGridLayout(cWidget)

        url = QtWidgets.QLabel("urls", cWidget)
        time = QtWidgets.QLabel("mins", cWidget)
        last = QtWidgets.QLabel("last check", cWidget)
        

        new_grid.addWidget(url,     0, 0)
        new_grid.addWidget(time,    0, 1)
        new_grid.addWidget(last,    0, 2)

        i = 1
        for tpl in running_threads:
            t = tpl[0]

            if(not tpl[1]):
                t.update_gui.connect(self._update_gui)
                tpl[1] = True

            url = QtWidgets.QLabel(t._url, cWidget)
            time = QtWidgets.QLabel(str(t._mins), cWidget)
            last = QtWidgets.QLabel(str(t._last_check), cWidget)
            button = QtWidgets.QPushButton("STOP", self)
            button.clicked.connect(self._make_pressed(t))

            new_grid.addWidget(url,     i, 0)
            new_grid.addWidget(time,    i, 1)
            new_grid.addWidget(last,    i, 2)
            new_grid.addWidget(button,  i, 3)


            i += 1

        cWidget.setLayout(new_grid)
        self.setCentralWidget(cWidget)
        
            

        