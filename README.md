# mycroft-status-icon
Nothing special, just a mycroft status icon for your system tray.  The
icon changes to recording when mycroft is listening, a gear when he's
processing, and everything he says gets displayed in a notification.  This
is useful for debugging.

The host/port `ws://127.0.0.1:9000/events/ws`is hardcoded.  You'll need to 
change it.  Perhaps in the future I'll have look in `/etc/` and 
`~/.mycroft/mycroft.ini`.

# Known bugs
- Doesn't reconnect quite right when you restart the service.

