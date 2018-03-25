#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

'''
负责存储批量的请求对象
对象接收到的请求进行去重判断，如果重复，就不进行存储
对外弹出请求对象，交给下载器去发起http请求
'''
# python3
# from queue import Queue
# <=python 2.7.13
# from Queue import Queue

from hashlib import sha1

# six兼容模块,py2 py3
# from six.moves.queue import Queue
import w3lib.url

from mini_scrapy.queue import Queue


class Scheduler(object):

    def __init__(self):
        self.queue = Queue()  # 使用redis的列表存储请求
        self.filter_set = set()  # 使用python集合对请求去重
        self.request_number = 0  # 记录发送的请求个数

    def add_reqeust(self, request):
        '''
        存储批量的请求对象
        :return:
        '''
        # 1. 先进行去重判断
        fp = self.fp_filter(request)
        if fp not in self.filter_set:
            self.filter_set.add(fp)
            self.queue.put(request)
            # 每添加一个，就记录一个
            self.request_number += 1

    def get_request(self):
        '''
        对外弹出请求对象
        :return:
        '''
        try:
            request = self.queue.get(False)
        except:
            return None
        else:
            return request

    def fp_filter(self, request):
        '''去重'''
        # 方案 利用hash算法sha1去求一个指纹，然后对指纹进行对比
        # 使用的数据:url method params data
        # 1.对url参数排序
        url = w3lib.url.canonicalize_url(request.url)
        # 2. params dict
        params = request.params if request.params is not None else {}
        params = str(sorted(params.items()))
        # 3. data dict
        data = request.data if request.data is not None else {}
        data = str(sorted(data.items()))

        s1 = sha1()
        s1.update(url.encode('utf-8'))
        s1.update(request.method.encode('utf-8'))
        s1.update(params.encode('utf-8'))
        s1.update(data.encode('utf-8'))

        return s1.hexdigest()
