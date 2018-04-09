#!/usr/bin/env python
# -*-coding:utf8-*-

from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets
from tornado.process import fork_processes
from functools import partial
from tornado import gen
from .apphandle import SyncHandle, AsyncHandle, ThreadHandle


class RouterConfig(Application):
    def _register(self, url, handler):
        super(RouterConfig, self).add_handlers(".*$", [(url, handler)])


class RpcServer(object):

    __route = []

    def __init__(self, app):
        self.app = app
        self.register(self.asyncGetRoute)

    def register(self, func):
        name = func.__name__
        handles = [SyncHandle, AsyncHandle, ThreadHandle]
        base = [h for h in handles if name.startswith(h.TYPE)].pop()
        handler = type(name, (base,), {'func': [func]})
        self.app._register("/{}".format(name), handler)
        self.__route.append(name)

    def start(self, app, port, multnum=1):
        sockets = bind_sockets(port)
        fork_processes(multnum)
        server = HTTPServer(app, xheaders=True)
        server.add_sockets(sockets)
        IOLoop.instance().start()

    @gen.coroutine
    def asyncGetRoute(self, *args, **kwargs):
        raise gen.Return([f for f in self.__route])

    @classmethod
    def _make_app(cls):
        return RouterConfig(cls.__route)

    @classmethod
    def init(cls, addr, multnum=1):
        _, port = addr.split(":", 1)
        app = cls._make_app()
        rpc_server = cls(app)
        rpc_server.start = partial(getattr(rpc_server, "start"), app=app,\
                                      port=port, multnum=multnum)
        return rpc_server
