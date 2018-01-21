# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from channels import Group


def ws_connect(message):
    Group('users').add(message.reply_channel)
    print(message)
    message.reply_channel.send({"accept": True})


def ws_disconnect(message):
    Group('users').discard(message.reply_channel)
    print(message)
    message.reply_channel.send({"accept": False})
