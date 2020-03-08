from abc import ABC, abstractmethod
from pydbus import SessionBus
from PyQt5 import QtWidgets, QtCore
import requests

NOTIFY_URL = 'https://us-central1-notify-15448.cloudfunctions.net/sendNotification?to={}&text={}&title={}'

#
# definition of the constants uniquely associated to a notification type. Each one must be a power of 2
# 
NO_NOTIFICATION = 0 
SYSTEM_NOTIFICATION = 1
WINDOW_NOTIFICATION = 2
PHONE_NOTIFICATION = 4

# 
# definition of the primitives used to unmask each notification type
# 

def is_system_notification(notifications: int) -> bool:
    return (notifications & SYSTEM_NOTIFICATION) != 0

def is_window_notification(notifications: int) -> bool:
    return (notifications & WINDOW_NOTIFICATION) != 0

def is_phone_notification(notifications: int) -> bool:
    return (notifications & PHONE_NOTIFICATION) != 0


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
        # TODO: send a signal which is received by the gui client
        pass


class PhoneNotification(Notification):
    def __init__(self, token, *args, **kwargs) -> None:
        super(PhoneNotification, self).__init__(*args, **kwargs)
        self.token = token

    def trigger(self) -> None:
        requests.get(NOTIFY_URL.format(self.token, self.text, self.title))


if __name__ == '__main__':
    SystemNotification().trigger()
    WindowNotification().trigger()
