from .notification import *
import requests
import logging 
import threading

logger = logging.getLogger(__name__)


class PageWatcher():
    """
    Object delegated to monitor a page
    """
    def __init__(self, url: str, check_time:float, *args, **kwargs) -> None:
        """
        url: the url of the page to monitor
        check_time: time in seconds between each check
        """
        super(PageWatcher, self).__init__(*args, **kwargs)
        
        self.url = url 
        self.check_time = check_time
        
        self.running_timer = None
        
        self.notifications = []

        self.initial_page = requests.get(self.url).text
        logger.info("Retrieved initial page")

    def start(self) -> None:
        """
        Start watching the url
        """
        self.running_timer = threading.Timer(self.check_time, self.__timer_expired)
        self.running_timer.start()
        
        logger.info("Starting timer")

    def stop(self) -> None:
        """
        Stop watching the url
        """
        if self.running_timer is not None:
            self.running_timer.cancel()
            logger.info("Stopping timer")
            self.running_timer = None
        else:
            logger.info("No timer is running")

    def __timer_expired(self) -> None:
        new_page = requests.get(self.url).text
        
        if new_page != self.initial_page:
            logger.info("Page changed, notifying...")
            self.__notify()
        else:
            logger.info("Page did not change")
            self.start()

    def __notify(self) -> None:
        for notification in self.notifications:
            notification.trigger()

    def add_notification(self, notification: Notification) -> None:
        """
        Add a new notification to be triggered when the page changes
        """
        self.notifications.append(notification)
        logger.info("Added new notification")

    def changed(self) -> bool:
        """
        :return True if the page changed, False otherwise
        """

        if self.running_timer is not None:
            logger.info("Page %s changed: %r", self.url, not self.running_timer.is_alive())
            return not self.running_timer.is_alive()
        else:
            logger.info("Page %s changed: False", self.url)
            return False

if __name__ == "__main__":
    url = 'https://www.lefrecce.it/B2CWeb/search.do?parameter=searchOutputViewer&cFID=XDgjk50ni8Mp'
    pw = PageWatcher(url, 1)
    pw.add_notification(SystemNotification())
    pw.start()
