#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

class SpiderMiddleware(object):

    def process_request(self, request):
        return request

    def process_item(self, item):
        return item


class DownloaderMiddleware(object):

    def process_request(self, request):
        return request

    def process_response(self, response):
        return response