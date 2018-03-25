#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

import redis
# redis键值对类型数据库
rd = redis.StrictRedis(host='localhost', port=6379, db=0)

a='123'
# 1. 利用返回值判断是否存在
ret = rd.set('filter_fp', a)

if ret == 0:
    print('存在')
else:
    print('bucunzai ')


ret = rd.sismember('filter_fp', a)
print(ret)  # True or False