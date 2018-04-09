#!/usr/bin/env python
# -*-coding:utf8-*-

from tornado.web import RequestHandler
from tornado import gen, log
import jwt
import base64
import traceback
import json
from functools import partial

class RequestBase(RequestHandler):

    __ALLOWEDUA__ = ('rpc')
    __SA = "tornadoRpc"

    @gen.coroutine
    def initialize(self):
        self.log = log.logging.getLogger()
        self.log.setLevel(log.logging.INFO)

    @gen.coroutine
    def prepare(self):
        '''
        ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NQ0o5LmV5Sl
        ZRU0k2SW5SdmNtNWhapRzlTY0dNaWZRLllJR2JaWmRkZX
        FKaGxLdXo3a2RQUjNMRpnlpT1Sa0ZNzFyZ3hONW9kRkpL
        dndRREJtR2txSUZaZXhEcHgzbGpM1TWpweFYxRENJalB3
        '''
        token = base64.b64decode(self.request.headers.get("X-Authorization-Token"))
        _AKey = self.request.headers.get("AKey")
        UA = self.request.headers.get("User-Agent")
        _key = jwt.decode(token, _AKey, ['HS512'])

        if _key.get('SA') != RequestBase.__SA and UA == 'rpclient':
            self.write_error(500)
            self.finish()

        parameter = json.loads(self.request.body)
        self.req_args = parameter['args']
        self.req_kwargs = parameter['kwargs']

    def func(self):
        raise Exception("None")

    def serialize(self, response=None, result=None):
        return json.dumps({"response":response, "result":result})

    def write_error(self, status_code, **kwargs):
        self.set_status(status_code)
        if status_code == 404:
            self.write('error:' + str(status_code))
        elif status_code == 500:
            self.write('error:{}'.format("Authentication error"))
        else:
            self.write('error:' + str(status_code))
        return
