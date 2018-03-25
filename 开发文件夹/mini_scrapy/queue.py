#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

import time
import pickle

import redis
from six.moves import queue as BaseQueue


# 接口同python的队列接口一直
class Queue(object):
    '''
    使用redis构建队列
    '''

    Empty = BaseQueue.Empty
    Full = BaseQueue.Full
    max_timeout = 0.3

    def __init__(self, name='request_queue', host='localhost', port=6379, db=1, maxsize=0, lazy_limit=True, password=None):
        '''
        :param name: 队列名
        :param host: IP地址
        :param port: 端口
        :param db: 数据库
        :param maxsize: 设置上限
        :param lazy_limit: 是否共享
        :param password: 密码
        '''
        self.name = name
        self.redis = redis.StrictRedis(host=host, port=port, db=db, password=password)
        self.maxsize = maxsize
        self.lazy_limit = lazy_limit
        self.last_qsize = 0

    def qsize(self):
        '''计算列表长度'''
        self.last_qsize = self.redis.llen(self.name)
        return self.last_qsize

    def empty(self):
        '''判断列表是否为空'''
        if self.qsize() == 0:
            return True
        else:
            return False

    def full(self):
        '''判断列表是否装满'''
        if self.maxsize and self.qsize() >= self.maxsize:
            return True
        else:
            return False

    def put_nowait(self, obj):
        '''判断是否可以在插入数据'''
        if self.lazy_limit and self.last_qsize < self.maxsize:
            pass
        elif self.full():
            # 如果超出列表长度抛出异常
            raise self.Full
        self.last_qsize = self.redis.rpush(self.name, pickle.dumps(obj))
        return True

    def put(self, obj, block=True, timeout=None):
        '''设置存储数据间隔时间,block为Flase则不设间隔时间'''
        if not block:
            return self.put_nowait(obj)

        start_time = time.time()
        while True:
            try:
                return self.put_nowait(obj)
            except self.Full:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)

    def get_nowait(self):
        ret = self.redis.lpop(self.name)
        if ret is None:
            raise self.Empty
        return pickle.loads(ret)

    def get(self, block=True, timeout=None):
        '''设置取数据间隔时间，block为False则不设置间隔时间'''
        if not block:
            return self.get_nowait()

        start_time = time.time()
        while True:
            try:
                return self.get_nowait()
            except self.Empty:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)