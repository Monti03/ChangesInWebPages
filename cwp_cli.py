from src.dbus import *
from src import notification
import pydbus
import argparse
import sys

DESCRIPTION='A commmand line interface for ChangesInWebPages'


parser = argparse.ArgumentParser("cwp-cli", description=DESCRIPTION)
subparsers = parser.add_subparsers(description="Available commands")
start_parser = subparsers.add_parser("start")
stop_parser = subparsers.add_parser("stop")
list_parser = subparsers.add_parser("list")
set_parser = subparsers.add_parser("set")


bus = pydbus.SessionBus()
watch_manager = bus.get(DBUS_ADDRESS, DBUS_WATCH_MANAGER_NAME)
print(watch_manager.list_watchers())
