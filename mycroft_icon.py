#!/usr/bin/env python

# Copyright 2016 Eugene R. Miller
#
# Mycroft icon is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# Mycroft Icon is distributed in the hope that it will
#  be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the Mycroft Icon.
# If not, see <http://www.gnu.org/licenses/>.


import gi
from gi.repository import Gtk
from pprint import pprint
from threading import Thread
import json
import subprocess
import sys
import websocket
from time import sleep

def on_message(ws, message):
    try:
        print "message:`%s`" % message
        msg = json.loads(message)
        pprint(msg)
        message_type = msg.get("message_type")
        if message_type == "speak":
            metadata = msg.get("metadata", {})
            said = metadata.get("utterance", "")
            if said:
                subprocess.check_output(["notify-send", "-i",
                                        "info",
                                         said])
        if message_type == "recognizer_loop:record_begin":
            print ("RECORD ICON")
            tray_icon.ind.set_from_stock(Gtk.STOCK_MEDIA_RECORD)
        if message_type == "recognizer_loop:record_end":
            print ("EXECUTE ICON")
            tray_icon.ind.set_from_stock(Gtk.STOCK_EXECUTE)
        if message_type in("recognizer_loop:utterance",
                           "recognizer_loop:audio_output_start"):
            print ("INFO ICON")
            tray_icon.ind.set_from_stock(Gtk.STOCK_INFO)
        if message_type in("recognizer_loop:audio_output_end"):
            print ("QUESTION ICON")
            tray_icon.ind.set_from_stock(Gtk.STOCK_DIALOG_QUESTION)

        while Gtk.events_pending():
            Gtk.main_iteration()
    except:
        e = sys.exc_info()[0]
        print("on_message error:", e)

def on_error(ws, error):
    tray_icon.ind.set_from_stock(Gtk.STOCK_DISCONNECT)
    sleep(10)
    # init_ws()
    print error

def on_close(ws):
    tray_icon.ind.set_from_stock(Gtk.STOCK_DISCONNECT)
    sleep(10)
    init_ws()
    print "### closed ###"

def on_open(ws):
    tray_icon.ind.set_from_stock(Gtk.STOCK_CONNECT)
    return

class TrayIcon():
    __name__ = 'TrayIcon'
    def __init__(self):
        self.init_icon()

    def init_icon(self):
        self.ind = Gtk.StatusIcon()
        self.ind.set_from_stock(Gtk.STOCK_DISCONNECT)

def start_ws():
    ws.run_forever()

def init_ws():
    print "init_ws()"
    tray_icon.ind.set_from_stock(Gtk.STOCK_DISCONNECT)
    websocket.enableTrace(True)
    global ws
    ws = websocket.WebSocketApp("ws://127.0.0.1:9000/events/ws",
        on_message = on_message,
        on_error = on_error,
        on_close = on_close
    )
    ws.on_open = on_open
    ws_thread = Thread(target=start_ws)
    ws_thread.start()

if __name__ == "__main__":
    tray_icon = TrayIcon()
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    init_ws()
    Gtk.main()
