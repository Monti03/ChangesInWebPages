from src.dbus import *
from src import notification
import pydbus
import argparse
import sys

DESCRIPTION='A commmand line interface for ChangesInWebPages'

#########################
# parser configuration 
#########################

parser = argparse.ArgumentParser("cwp-cli", description=DESCRIPTION)
subparsers = parser.add_subparsers(description="Available commands")

start_parser = subparsers.add_parser("start", help="start watching a certain url")
start_parser.add_argument("check_time", metavar="CHECK_TIME", type=float, help="Time (in secs) between each check")
start_parser.add_argument("url", metavar="URL", type=str, help="The url to be monitored")
start_parser.add_argument("-pn", "--phone-notification", action="store_true", help="send a notification to the phone (may need --token if was not previously set)")
start_parser.add_argument("-wn", "--window-notification", action="store_true", help="send a notification on the desktop if the gui client is running")
start_parser.add_argument("-sn", "--system-notification", action="store_true", help="send a system notification")
start_parser.add_argument("--token", type=str, help="the token used to send the phone notification")

stop_parser = subparsers.add_parser("stop", help="stop a watcher")
stop_parser.add_argument("wid", metavar="ID", type=int, help="the id of the watcher to stop")

list_parser = subparsers.add_parser("list", help="list the runnning watchers")

set_parser = subparsers.add_parser("set", help="configure a certain variable")
set_parser.add_argument("--token", metavar="TOKEN", type=str, help="the token to use for phone notifications")

parser.parse_args()

########################
# bus configuration 
########################

bus = pydbus.SessionBus()
watch_manager = bus.get(DBUS_ADDRESS, DBUS_WATCH_MANAGER_NAME)
print(watch_manager.list_watchers())
