from pyforms.basewidget import BaseWidget
from pyforms.controls   import ControlFile
from pyforms.controls   import ControlText
from pyforms.controls   import ControlSlider
from pyforms.controls   import ControlPlayer
from pyforms.controls   import ControlButton
from pyforms.controls   import ControlLabel
from pyforms.controls   import ControlCheckBox
from pyforms            import start_app
from threading          import Thread
from letturaSito        import read
from sendMail           import sendMessage
from sendMail           import sign
import time
import datetime
import sys
import os

class MyGui(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('WebPageChange')

        
        self._url               = ControlText('Url')
        self._notifyToken       = ControlText('NotifyToken')
        self._checkbox          = ControlCheckBox("notification")
        self._period            = ControlSlider('Period', default=10, minimum=1, maximum=360)
        self._runbutton         = ControlButton('Run')
        self._state_labe        = ControlLabel("In Attesa Dell'Url")
        self._runbutton.value   = self.__runEvent
        self._state             = 0

        self._formset = [
            ('_url'),
            ('_notifyToken','_checkbox'),
            ('_period', '_runbutton'),
            ('_state_labe')
        ]

    def __runEvent(self):
        if(self._state == 0 and self._url.value != '' and self.__controllNotification()):
            self.th = ControllThread(self._url.value, self._period.value, self)
            self.th.start()
            self._state_labe.value = "Scansionando"
            self._state = 1
    
    def __controllNotification(self):
        if(self._notifyToken.value == '' and self._checkbox.value):
            print(os.environ["HOME"])
            if(os.path.exists(os.environ["HOME"]+"/.notifyreg")):
                return True
            else:
                self.success("Devi inserire il token per potere avere le notifiche", title=None)
                return False
        else:
            if(os.path.exists(os.environ["HOME"]+"/.notifyreg")):
                return True
            else:
                sign(self._notifyToken.value)
                return True
                
    def __CloseAction(self):
        sys.exit()

class ControllThread(Thread):
 
    def __init__(self,url,mins,my_gui):
        ''' Constructor. '''
        Thread.__init__(self)
        self._mins   = mins
        self._url    = url 
        self._my_gui = my_gui
        self._flag   = True
 
    def run(self):
               
        text = read(self._url)
        print("ok")
        condition = True
        i = 0
        while(condition and self._flag):
            time.sleep(self._mins*60)
            condition = text == read(self._url)
            #print(datetime.datetime.now())
            self._my_gui._state_labe.value = time.strftime("%H:%M:%S",time.gmtime())

        if(self._my_gui._checkbox.value):
            sendMessage(self._url)
        self._my_gui.success("cambiamento", title=None)

    def stop(self):
        self._flag = False



if __name__ == '__main__':
    w = start_app(MyGui, geometry=(100, 100, 400, 100))