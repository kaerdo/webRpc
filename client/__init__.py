#!/usr/bin/env python
# -*-coding:utf8-*-

import requests
import os
from functools import partial
import json
import jwt
import base64

class Rpclient(object):
    def __init__(self, server):
        self.server = server
        response = self.asyncGetRoute()
        map(lambda x: setattr(self, x, RpcRequest(self.server, x)),
            [func for func in response]
            )

    def __getattr__(self, endpoint):
        return RpcRequest(self.server, endpoint)


class RpcRequest(object):

    __KEY = "L19ndC90aW1l"
    __SA = "tornadoRpc"

    def __init__(self, server, endpoint):
        _token = self.encryption()
        __header = {'User-Agent': 'rpclient',
                    'Content-Type': 'application/json',
                    'X-Authorization-Token': _token,
                    'AKey': RpcRequest.__KEY
                    }
        if not server.startswith("http://"):
            server = "http://" + server
        url = os.path.join(server, endpoint)
        self.request_client = partial(requests.post, url, headers=__header)

    def encryption(self):
        _key = jwt.encode({'SA': self.__SA}, self.__KEY, 'HS512').decode()
        token = base64.b64encode(_key)
        return token

    def __call__(self, *args, **kwargs):
        data = {}
        data["args"] = args
        data["kwargs"] = kwargs
        data = json.dumps(data)
        try:
            response = self.request_client(data=data)
        except Exception:
            raise Exception("The request failed")
        else:
            if response.status_code == 200:
                data = json.loads(response.content)
                if data.get("result") == "succeed":
                    return data.get("response")
        raise Exception("request failed")

