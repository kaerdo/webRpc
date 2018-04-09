#!/usr/bin/env python
# -*-coding:utf8-*-

from client import Rpclient

R = Rpclient("127.0.0.1:9898")
print R.sync_getime(days=2)
print R.async_webrequest("http://www.baidu.com")
print R.thread_sleep(3)