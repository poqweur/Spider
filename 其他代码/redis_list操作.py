#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY


import pickle  # 对象序列化

import redis
# redis键值对类型数据库
rd = redis.StrictRedis(host='localhost', port=6379, db=1)



class Request(object):

    def __init__(self, url, method='GET', headers=None, params=None, data=None, parse='parse'):
        self._url = url
        self._method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.parse = parse

request = Request('asda')
print(request)
ret = pickle.dumps(request)
print(rd.lpush('request_queue', ret))


ret2 = rd.rpop('request_queue')
request = pickle.loads(ret2)
print(request)
# 往列表左边插入
# rd.lpush()
# # 右侧插入
# rd.rpush()
# # 左侧弹出
# rd.lpop()
# # 右侧弹出
# rd.rpop()