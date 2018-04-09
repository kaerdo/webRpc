# WebRpc

撸了一个http RPC，效率还可以

1. 支持三种模式 同步 异步 线程
2. 支持token
3. 线程池没使用tornado的ThreadPoolExecutor 自带的功能较弱. 自己实现了一个,可支持优先级,稍后再精简下会push上来.

   函数注册有命名规则 "模式+自定义"

注册：
```
s = RpcServer.init(options.addr)
s.register(async_webrequest)
s.register(sync_getime)
s.register(thread_sleep)
s.start()

```

请求：
```
from client import Rpclient

R = Rpclient("127.0.0.1:9898")
print R.sync_getime(days=2)
print R.async_webrequest("http://www.baidu.com")
print R.thread_sleep(3)

```
