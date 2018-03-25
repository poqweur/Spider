#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

'''
根据请求信息，发出http请求，获取http响应
返回一个http响应
'''

import re
import json

from lxml import etree
import requests

from mini_scrapy.utils.log import logger


class Response(object):

    def __init__(self, url, headers, content, status_code, request):
        self.url = url  # 响应url
        self.headers = headers  # 响应头
        self.content = content  # 响应体
        self.status_code = status_code  # 状态码
        self.request = request

    def xpath(self, rule):
        '''对xpath封装'''
        html = etree.HTML(self.content)
        return html.xpath(rule)

    def re_math(self, rule, data=None):
        '''
        对正则match方法封装
        :param rule: 正则规则
        :param data: 默认是content
        :return:
        '''
        if data is None:
            data = self.content
        return re.match(rule, data)

    @property
    def json(self):
        return json.loads(self.content)

class Downloader(object):

    timeout = 2

    def get_response(self, request):
        '''
        根据请求信息，发出http请求，获取http响应
        :return:
        '''
        # 1. 判断请求方法
        response = None

        if request.method == 'GET':
            response = requests.get(request.url, headers=request.headers, params=request.params, timeout=self.timeout)
            logger.info("[%d] %s" % (response.status_code, response.url))
        elif request.method == 'POST':
            response = requests.post(request.url, headers=request.headers, params=request.params, data=request.data, timeout=self.timeout)
            logger.info("[%d] %s"%(response.status_code, response.url))
        return Response(response.url, response.headers, response.content, response.status_code, request)