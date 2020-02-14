#!/usr/bin/env python3

from PyQt5              import QtGui, QtWidgets, QtCore

from threading          import Thread
from read_pages         import read
from read_pages         import check_url
from notification       import send_message
from notification       import sign
from menu               import Menu
from menu               import running_threads

import time
import datetime
import sys
import os

START_NOTIFICATION = "Now I'm controlling {} each {} minutes.\nIf you whant to stop it go to Menu->Thread or CTRL+M"

class MainWindow(QtWidgets.QMainWindow):
    #to notify the menu gui of changes
    main_gui_notification_to_menu = QtCore.pyqtSignal(object)

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.setWindowTitle('Changes In Web Pages')
        self.resize(600, 250)
        self.setWindowIcon(QtGui.QIcon('media/logo.png'))
        
        cWidget = QtWidgets.QWidget(self)

        #menu
        menu_action = QtWidgets.QAction("Threads", self)
        menu_action.setShortcut("Ctrl+M")
        menu_action.triggered.connect(self._show_menu)

        menu = self.menuBar().addMenu('Menu')
        menu.addAction(menu_action)

        #grid
        grid = QtWidgets.QGridLayout(cWidget)

        #labels
        self._labelurl = QtWidgets.QLabel("Url", cWidget)
        self._labelnotify = QtWidgets.QLabel("Notify Token", cWidget)
        self._show_mins = QtWidgets.QLabel("Minutes: 10", cWidget)

        #texts
        self._url = QtWidgets.QLineEdit(self)
        self._url.resize(500,20)
        self._notify_token = QtWidgets.QLineEdit(self)

        #check box
        self._check_box = QtWidgets.QCheckBox("Notification", cWidget)
        self._check_box.setChecked(True)

        #start button
        self._start_button = QtWidgets.QPushButton("Start", self)
        self._start_button.clicked.connect(self._start)

        #slider
        self._mins = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self._mins.setMinimum(1)
        self._mins.setMaximum(360)
        self._mins.setValue(10)
        self._mins.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self._mins.setTickInterval(10)
        
        self._mins.valueChanged.connect(self._change_in_slider)

        #adding elements to the grid
        grid.addWidget(self._labelurl,     0, 0)
        grid.addWidget(self._labelnotify,  1, 0)

        grid.addWidget(self._url,          0, 1)
        grid.addWidget(self._notify_token, 1, 1)
        grid.addWidget(self._check_box,    1, 2)        

        grid.addWidget(self._mins,         2, 1)
        grid.addWidget(self._start_button, 2, 2)

        grid.addWidget(self._show_mins, 2, 0)

        #setting layout
        cWidget.setLayout(grid)
        self.setCentralWidget(cWidget)    

        #starting menu
        self._menu_gui = Menu(self)

    #called when the user go to menu -> threads or use CTRL+M
    #updates the menu and shows it
    def _show_menu(self):
        self.main_gui_notification_to_menu.emit('-\n' % ())
        self._menu_gui.show()

    #changes the value near Minutes to make it conicide with the value on the slider
    def _change_in_slider(self):
        size = self._mins.value()
        self._show_mins.setText("Minutes: {}".format(size))

    #start a new thread that controls url
    def _start(self):
        if(self._url.text() != '' and self._control()):

            tmp_url = self._url.text()
            if("http://" not in tmp_url and "https://" not in tmp_url):
                self._url.setText("http://{}".format(tmp_url))

            print(self._url.text())
            if(not check_url(self._url.text())):
                QtWidgets.QMessageBox.information(self, 'Problem!',"The url you insert is not valid")
                return
            
            th = ControlThread(self._url.text(), self._mins.value(), self._check_box.isChecked(), self)
            th.changed.connect(self._on_change)
            th.start()
            running_threads.append([th, False])
            self._url.setText("")
            QtWidgets.QMessageBox.information(self, "Started" ,START_NOTIFICATION.format(self._url.text(), str(self._mins.value())))
            
    #function that is executed by the Gui thread when a ControlThread calls self.update_gui.emit('-\n' % ())
    def _on_change(self, url):
        QtWidgets.QMessageBox.information(self, 'Has changed!',"this url:{} has changed".format(url))

    #function that controls data before start a new ControlThread
    def _control(self):
        if(not self._check_box.isChecked()):
            return True

        if(self._notify_token.text() == '' and self._check_box.isChecked()):
            print(os.environ["HOME"])
            if(os.path.exists("./.device_id")):
                return True
            else:
                QtWidgets.QMessageBox.information(self, 'Problem!',"if you whant notification on the phone you must set notification token")
                return False
        else:
            #registers user notify_token
            sign(self._notify_token.text())
            return True

#thread class that controls urls
class ControlThread(QtCore.QThread):

    #signal object to notify menu gui and main gui
    changed = QtCore.pyqtSignal(object)
    update_gui = QtCore.pyqtSignal(object)

    def __init__(self,url,mins,check_box_value,my_gui):
        QtCore.QThread.__init__(self)
        self._mins   = mins
        self._url    = url 
        self._my_gui = my_gui
        self._check_box_value = check_box_value #if True -> the notification is also send to the phone
        self._flag   = True                     #if True the Thread has been not stopped from the Menu
        self._last_check = time.strftime("%H:%M:%S",time.localtime())
 
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
            self._last_check = time.strftime("%H:%M:%S",time.localtime())

            self.update_gui.emit('-\n' % ())    #menu gui update -> is updated _last_check

        if(self._check_box_value and self._flag):
            send_message(self._url)

        if(self._flag):
            self.changed.emit('%s\n' % (self._url))
            if([self,True] in running_threads):
                running_threads.remove([self,True])
            else:
                running_threads.remove([self,False])
        
        self.update_gui.emit('-\n' % ())         #to remove this thread form the menu gui
                
            
    def stop(self):
        self._flag = False

        if([self,True] in running_threads):
            running_threads.remove([self,True])
        elif [self,False] in running_threads:
            running_threads.remove([self,False])

        self.update_gui.emit('-\n' % ())        #to remove this thread form the menu gui

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
