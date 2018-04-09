#!/usr/bin/env python
# -*-coding:utf8-*-

from .webhandle import RequestBase
from tornado import gen
from functools import partial
from .task import ThreadTask, TaskManage

class SyncHandle(RequestBase):

    TYPE = 'sync'

    def post(self, *args, **kwargs):
        try:
            data = self.func[0](*self.req_args, **self.req_kwargs)
            result = "succeed"
        except Exception, e:
            data = e
            result = "failed"
        self.write(self.serialize(data, result))

class AsyncHandle(RequestBase):

    TYPE = 'async'

    @gen.coroutine
    def post(self, *args, **kwargs):
        try:
            data = yield self.func[0](*self.req_args, **self.req_kwargs)
            result = "succeed"
        except Exception, e:
            data = e
            result = "failed"
        self.write(self.serialize(data, result))

class ThreadHandle(RequestBase):

    TYPE = 'thread'

    @gen.coroutine
    def post(self, *args, **kwargs):
        taskmanage = TaskManage()
        func = partial(self.func[0], *self.req_args, **self.req_kwargs)
        # t = ThreadTask(0, func=func)
        data = yield gen.Task(taskmanage.enqueue, func)
        result = "succeed"
        self.write(self.serialize(data, result))


