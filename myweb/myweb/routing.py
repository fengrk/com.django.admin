# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from channels.routing import route

from poll.consumers import ws_connect, ws_disconnect

channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
]
