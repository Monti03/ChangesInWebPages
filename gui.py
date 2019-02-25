#!/usr/bin/python

from PyQt4              import QtGui, QtCore

from threading          import Thread
from read_pages         import read
from notification       import send_message
from notification       import sign
from menu               import Menu
from menu               import running_threads

import time
import datetime
import sys
import os

START_NOTIFICATION = "Now I'm controlling {} each {} minutes.\nIf you whant to stop it go to Menu->Thread or CTRL+M"

class MainWindow(QtGui.QMainWindow):

    main_gui_notification_to_menu = QtCore.pyqtSignal(object)

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

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
        self._show_mins = QtGui.QLabel("Minutes: 10", cWidget)

        #texts
        self._url = QtGui.QLineEdit(self)
        self._url.resize(500,20)
        self._notify_token =  QtGui.QLineEdit(self)

        #check box
        self._check_box = QtGui.QCheckBox("Notification", cWidget)
        self._check_box.setChecked(True)

        #start button
        self._start_button = QtGui.QPushButton("Start", self)
        self._start_button.clicked.connect(self._start)

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

        self._menu_gui = Menu(self)

    def _show_menu(self):
        self.main_gui_notification_to_menu.emit('-\n' % ())
        self._menu_gui.show()

    def _change_in_slider(self):
        size = self._mins.value()
        self._show_mins.setText("Minutes: {}".format(size))


    def _start(self):
        if(self._url.text() != '' and self._controll()):
            th = ControllThread(self._url.text(), self._mins.value(), self._check_box.isChecked(), self)
            th.changed.connect(self._on_change)
            th.start()
            running_threads.append([th, False])
            self._url.setText("")
            QtGui.QMessageBox.information(self, "Started" ,START_NOTIFICATION.format(self._url.text(), str(self._mins.value())))
            
    
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
    update_gui = QtCore.pyqtSignal(object)
    
    def __init__(self,url,mins,check_box_value,my_gui):
        ''' Constructor. '''
        QtCore.QThread.__init__(self)
        self._mins   = mins
        self._url    = url 
        self._my_gui = my_gui
        self._check_box_value = check_box_value
        self._flag   = True
        self._last_check = time.strftime("%H:%M:%S",time.gmtime())
 
    def run(self):
        
        text = read(self._url)
        condition = True
        i = 0
        while(condition):
            condition = text == read(self._url)
            if(not condition):
                break
            time.sleep(self._mins*60)
            if(not self._flag):
                return
            self._last_check = time.strftime("%H:%M:%S",time.gmtime())

            self.update_gui.emit('-\n' % ())

        if(self._check_box_value and self._flag):
            send_message(self._url)

        if(self._flag):
            self.changed.emit('%s\n' % (self._url))
            if([self,True] in running_threads):
                running_threads.remove([self,True])
            else:
                running_threads.remove([self,False])
        
        self.update_gui.emit('-\n' % ())
                
            
    def stop(self):
        self._flag = False

        if([self,True] in running_threads):
            running_threads.remove([self,True])
        elif [self,False] in running_threads:
            running_threads.remove([self,False])

        self.update_gui.emit('-\n' % ())

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())