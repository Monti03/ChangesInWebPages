from abc import ABC, abstractmethod
from pydbus import SessionBus
from PyQt5 import QtWidgets, QtCore
import requests

NOTIFY_URL = 'https://us-central1-notify-15448.cloudfunctions.net/sendNotification?to={}&text={}&title={}'


class Notification(ABC):
    """
    A notification object. When triggered sends the notification
    """
    def __init__(self, title: str="Cwp", text: str="A page just changed") -> None:
        super().__init__()
        self.title = title
        self.text = text

    @abstractmethod
    def trigger(self) -> None:
        """
        Sends the notification
        """
        pass


class SystemNotification(Notification):
    def __init__(self, mstime: int=5000, *args, **kwargs) -> None:
        super(SystemNotification, self).__init__(*args, **kwargs)
        self.mstime = mstime

    def trigger(self) -> None:
        """
        Sends a system notification
        """
        bus = SessionBus()
        notifications = bus.get('.Notifications')

        notifications.Notify('cwp', 0, 'dialog-information', self.title, self.text, [], {}, self.mstime)


class WindowNotification(Notification):
    """
    A window notification object. Needs a running Qt application in order to be sent
    """
    def __init__(self, *args, **kwargs) -> None:
        super(WindowNotification, self).__init__(*args, **kwargs)

    def trigger(self) -> None:
        """
        Open a new window with for the notification
        """
        # create a QApplication and a QMainWindow, which are needed to open a dialog window
        app = QtWidgets.QApplication([])
        QtWidgets.QMessageBox.information(QtWidgets.QMainWindow(), self.title, self.text)


class PhoneNotification(Notification):
    def __init__(self, token, *args, **kwargs) -> None:
        super(PhoneNotification, self).__init__(*args, **kwargs)
        self.token = token

    def trigger(self) -> None:
        requests.get(NOTIFY_URL.format(self.token, self.text, self.title))


if __name__ == '__main__':
    SystemNotification().trigger()
    WindowNotification().trigger()
    PhoneNotification('EmUXaAu').trigger()
