#!/usr/bin/env python3

from src.dbus import *
from src import notification as notifications_module
import pydbus
import argparse
import sys
import tabulate

DESCRIPTION='A commmand line interface for ChangesInWebPages'

#########################
# parser configuration 
#########################

parser = argparse.ArgumentParser("cwp-cli", description=DESCRIPTION)
subparsers = parser.add_subparsers(description="Available commands", dest="command")

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

get_parser = subparsers.add_parser("get", help="get the current value of a certain variable")
get_parser.add_argument("--token", action="store_true", help="the value of the token used for phone notifications")

parsed_args = parser.parse_args()

########################
# bus configuration 
########################

bus = pydbus.SessionBus()
watch_manager = bus.get(DBUS_ADDRESS, DBUS_WATCH_MANAGER_NAME)

if parsed_args.command == "start":
    if parsed_args.token is not None:
        watch_manager.set_token(parsed_args.token)

    notifications = notifications_module.NO_NOTIFICATION
    if parsed_args.phone_notification is not None:
        notifications += notifications_module.PHONE_NOTIFICATION
    if parsed_args.window_notification is not None:
        notifications += notifications_module.WINDOW_NOTIFICATION
    if parsed_args.system_notification is not None:
        notifications += notifications_module.SYSTEM_NOTIFICATION
    
    watch_manager.start_watching(parsed_args.url, parsed_args.check_time, notifications)
elif parsed_args.command == "stop":
    watch_manager.stop_watching(parsed_args.wid)
elif parsed_args.command == "list":
    print(tabulate.tabulate(watch_manager.list_watchers(), headers=["ID", "url", "check_time"]))
elif parsed_args.command == "set":
    if parsed_args.token is not None:
        watch_manager.set_token(parsed_args.token)
elif parsed_args.command == "get":
    if parsed_args.token:
        print(watch_manager.get_token())
