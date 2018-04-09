#!/usr/bin/env python
# -*-coding:utf8-*-

from server import RpcServer
from tornado import gen
from tornado.options import options, define
from tornado.httpclient import AsyncHTTPClient
import datetime
import time

define("addr", default="127.0.0.1:9898", type=str, help="Valid request address")

def thread_sleep(seconds):
    for i in range(seconds):
        time.sleep(1)
        print "say hi"
    return "Has been completed"

def sync_getime(days):
    data = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y%m%d')
    return str(data)

@gen.coroutine
def async_webrequest(url):
    client = AsyncHTTPClient()
    response = yield gen.Task(client.fetch, url)
    data = response.body
    raise gen.Return(data)

if __name__ == "__main__":
    options.parse_command_line()
    s = RpcServer.init(options.addr)
    s.register(async_webrequest)
    s.register(sync_getime)
    s.register(thread_sleep)
    s.start()


