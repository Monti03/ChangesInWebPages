#!/usr/bin/python

from PyQt4              import QtGui, QtCore

from threading          import Thread
from read_pages         import read
from notification       import send_message
from notification       import sign
from menu               import Menu

import time
import datetime
import sys
import os

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self._inrunning = 0
        self._running_threads = []

        self.setWindowTitle('Changes In Web Pages')
        self.resize(600, 250)
        self.setWindowIcon(QtGui.QIcon('media/logo.png'))
        
        cWidget = QtGui.QWidget(self)

        #menu
        menu_action = QtGui.QAction("Threads", self)
        menu_action.setShortcut("Ctrl+M")
        menu_action.triggered.connect(self._show_menu)

        menu = self.menuBar().addMenu('Menu')
        menu.addAction(menu_action)

        #grid
        grid = QtGui.QGridLayout(cWidget)

        #labels
        self._labelurl = QtGui.QLabel("Url", cWidget)
        self._labelnotify = QtGui.QLabel("Notify Token", cWidget)
        self._show_mins = QtGui.QLabel("Minutes:10", cWidget)

        #texts
        self._url = QtGui.QLineEdit(self)
        self._url.resize(500,20)
        self._notify_token =  QtGui.QLineEdit(self)

        #check box
        self._check_box = QtGui.QCheckBox("Notification", cWidget)
        self._check_box.setChecked(True)

        #start button
        self._start_button = QtGui.QPushButton("Toggle button")
        self._start_button.setCheckable(True)

        self.connect(self._start_button, QtCore.SIGNAL('clicked()'), self._start)

        #slider
        self._mins = QtGui.QSlider(QtCore.Qt.Horizontal)
        self._mins.setMinimum(1)
        self._mins.setMaximum(360)
        self._mins.setValue(10)
        self._mins.setTickPosition(QtGui.QSlider.TicksBelow)
        self._mins.setTickInterval(10)
        
        self._mins.valueChanged.connect(self._change_in_slider)

        grid.addWidget(self._labelurl,     0, 0)
        grid.addWidget(self._labelnotify,  1, 0)

        grid.addWidget(self._url,          0, 1)
        grid.addWidget(self._notify_token, 1, 1)
        grid.addWidget(self._check_box,    1, 2)        

        grid.addWidget(self._mins,         2, 1)
        grid.addWidget(self._start_button, 2, 2)

        grid.addWidget(self._show_mins, 2, 0)

        cWidget.setLayout(grid)
        self.setCentralWidget(cWidget)


    def _show_menu(self):
        self._menu_gui = Menu(self)
        self._menu_gui.show()

    def _change_in_slider(self):
        size = self._mins.value()
        self._show_mins.setText("Minutes:{}".format(size))


    def _start(self):
        if(self._url.text() != '' and self._controll()):
            th = ControllThread(self._url.text(), self._mins.value(), self._check_box.isChecked(), self)
            th.changed.connect(self._on_change)
            th.start()
            print(self._url.text())
            self._running_threads.append(th)
            self._inrunning += 1
            #self._state_in_run.value = "in running:{}".format(self._inrunning)
    
    def _on_change(self, url):
        QtGui.QMessageBox.information(self, 'Has changed!',"this url:{} has changed".format(self._url.text()))

    def _controll(self):
        if(not self._check_box.isChecked()):
            return True

        if(self._notify_token.text() == '' and self._check_box.isChecked()):
            print(os.environ["HOME"])
            if(os.path.exists(os.environ["HOME"]+"/.notifyreg")):
                return True
            else:
                QtGui.QMessageBox.information(self, 'Problem!',"if you whant notification on the phone you must set notification token")
                return False
        else:
            if(os.path.exists(os.environ["HOME"]+"/.notifyreg")):
                return True
            else:
                sign(self._notify_token.text())
                return True

class ControllThread(QtCore.QThread):

    changed = QtCore.pyqtSignal(object)
 
    def __init__(self,url,mins,check_box_value,my_gui):
        ''' Constructor. '''
        QtCore.QThread.__init__(self)
        self._mins   = mins
        self._url    = url 
        self._my_gui = my_gui
        self._check_box_value = check_box_value
        self._flag   = True
        self._last_check = 0
 
    def run(self):
        
        text = read(self._url)
        condition = True
        i = 0
        while(condition and self._flag):
            time.sleep(self._mins*60)
            condition = text == read(self._url)
            self._last_check = time.strftime("%H:%M:%S",time.gmtime())

        if(self._check_box_value):
            send_message(self._url)
        self.changed.emit('%s\n' % (self._url))

    def stop(self):
        self._flag = False


app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())