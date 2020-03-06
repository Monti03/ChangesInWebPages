import pydbus
import logging
import sys
from gi.repository import GLib
from src.watch_manager import *
from src.dbus import *

#
# set up logger
#

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s'))


# open session bus
bus = pydbus.SessionBus()
logger.info("Opened session bus")

# register name for the service
bus.request_name(DBUS_ADDRESS)

# expose object
bus.publish(DBUS_ADDRESS + '.' + DBUS_WATCH_MANAGER_NAME, WatchManager())

# start watching on published objects
loop = GLib.MainLoop()
loop.run()
