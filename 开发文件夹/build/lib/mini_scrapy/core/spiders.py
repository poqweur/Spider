#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY


'''
程序一开始时，提供初始请求对象
提供解析响应的方法，负责返回提取的数据或新增的请求对象
'''


class Request(object):

    def __init__(self, url, method='GET', headers=None, params=None, data=None, parse='parse'):
        self._url = url
        self._method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.parse = parse

    @property
    def url(self):
        return self._url

    @property
    def method(self):
        return self._method.upper()


class Spider(object):

    start_url = None

    def start_requests(self):
        '''
        提供初始请求对象
        :return:
        '''
        return [Request(self.start_url)]

    def parse(self, response):
        '''
        解析响应的方法，负责返回提取的数据或新增的请求对象
        :return:
        '''

        return response.content


