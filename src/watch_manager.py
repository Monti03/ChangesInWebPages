from .page_watcher import *
import logging

logger = logging.Logger(__name__)


class WatchManager():
    """
    <node>
      <interface name='com.github.changesinwebpages.WatchManager'>
       <method name='start_watching'>
          <arg type='s' name='url' direction='in'/>
          <arg type='d' name='check_time' direction='in'/>
          <arg type='i' name='notifications' direction='in'/>
        </method>
        <method name='stop_watching'>
          <arg type='i' name='id' direction='in'/>
        </method>
        <method name='list_watchers'>
          <arg type='a{i(si)}' name='l' direction='out'/>
        </method>
        <method name='get_token'>
          <arg type='s' name='token' direction='out'/>
        </method>
        <method name='set_token'>
          <arg type='s' name='token' direction='in'/>
        </method>
      </interface>
    </node>
    """
    def __init__(self, *args, **kwargs) -> None:
        super(WatchManager, self).__init__(*args, **kwargs)
        
        self.watcher_id = 0
        self.watchers = {}
        self.token = "" 

    def set_token(self, token:str) -> None:
        logger.info("New token: " + token)
        self.token = token

    def get_token(self) -> str:
        return self.token

    def start_watching(self, url: str, check_time: float, notifications: int) -> None:
        """
        Start monitoring the page with the given url each check_time number of seconds. notifications is a mask obtained by summing the constants defined in notifications.py, 
        each corresponding to a different type. If the phone notification is required the token must be set at least once with the set_token() function, otherwise it will not 
        be sent
        """
        watcher = PageWatcher(url, check_time)
        
        self.watchers[self.watcher_id] = watcher
        self.watcher_id += 1

        if is_system_notification(notifications):
            watcher.add_notification(SystemNotification())
        if is_window_notification(notifications):
            watcher.add_notification(WindowNotification())
        if is_phone_notification(notifications) and self.token != "":
            watcher.add_notification(PhoneNotification(self.token))

        watcher.start()
        logger.info("New watcher created for " + url)

    def stop_watching(self, watcher_id: int) -> None:
        """
        Stops the watcher with the specifies id
        """
        try:
            watcher = self.watchers.pop(watcher_id)
            watcher.stop()
            logger.info("Removed watcher with id " + str(watcher_id))
        except KeyError:
            logger.info("Watcher with id " + watcher_id + " not found")

    def list_watchers(self) -> dict:
        """
        Returns a list of the running watcher with their id
        """
        return {k: (v.url, v.check_time) for k, v in self.watchers.items()}


if __name__ == "__main__":
    manager = WatchManager()
    url = 'https://www.lefrecce.it/B2CWeb/search.do?parameter=searchOutputViewer&cFID=8IYnABwHYCRo'
    manager.start_watching(url, 5, SYSTEM_NOTIFICATION)
    print(manager.list_watchers())
