#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

import types
import time
from datetime import datetime

import gevent  # 仅对于IO操作，比如文件写入或者网络 socket
# 使用协程补丁
from gevent import monkey
monkey.patch_all()  # 替换掉socket，变成非阻塞模式。注意线程一定不要开启补丁程序会无法退出

from mini_scrapy.async.cor import Pool  # 协程池
# from mini_scrapy.async.thread import Pool  # 线程池
# from mini_scrapy.async.multiprocessing import Pool  # 进程池,需要更改队列存储
from mini_scrapy.utils.log import logger
from mini_scrapy.conf import settings

from .spiders import Request
from .scheduler import Scheduler
from .downloader import Downloader
from .pipline import Pipeline

class Engine(object):

    def __init__(self, spiders, spider_mids=[], downloader_mids=[]):
        self.spiders = spiders  # 爬虫
        self.scheduler = Scheduler()  # 调度器
        self.downloader = Downloader()  # 下载器
        self.pipline = Pipeline()  # 管道
        self.spider_mids = spider_mids  # 爬虫中间件
        self.downloader_mids = downloader_mids  # 下载中间件

        self.pool = Pool()

        self.response_number = 0  # 响应数量

        self.max_async = settings.MAX_ASYNC  # 最大并发数

        self.running = False

    def _execute_start_requests(self):
        # 1.调用爬虫的strat
        for spider_name, spider in self.spiders.items():
            requests_ = spider.start_requests()
            for request in requests_:
                # 加入爬虫中间件
                for spider_mid in self.spider_mids:
                    request = spider_mid.process_request(request)

                # 2.把请求对象交给调度器
                request.spider_name = spider.name
                self.scheduler.add_reqeust(request)

    def _execute_request_response_item(self):
        # 3.从调度器取出请求，并交给下载
        # 3.1
        request = self.scheduler.get_request()
        if request is None:
            return

        # 加入下载中间件
        for downloader_mid in self.downloader_mids:
            request = downloader_mid.process_request(request)

        # 3.2
        response = self.downloader.get_response(request)

        # 加入卸载中间件
        for downloader_mid in self.downloader_mids:
            response = downloader_mid.process_request(response)

        # 4.交给爬虫去解析
        spider = self.spiders[response.request.spider_name]
        # 从爬虫中获取对应的解析方法
        parse = getattr(spider, response.request.parse)

        result = parse(response)

        if isinstance(result, types.GeneratorType):
            for r in result:
                # 5.判断result是不是Request对象
                if type(r) == Request:  # 如果是
                    # 加入中间件
                    for spider_mid in self.spider_mids:
                        r = spider_mid.process_request(r)
                    r.spider_name = spider.name
                    self.scheduler.add_reqeust(r)
                else:
                    for spider_mid in self.spider_mids:
                        r = spider_mid.process_item(r)
                    self.pipline.process_item(r)
        else:
            # 5.判断result是不是Request对象
            if type(result) == Request:  # 如果是
                # 加入中间件
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_request(result)
                result.spider_name = spider.name
                self.scheduler.add_reqeust(result)
            else:
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_item(result)
                self.pipline.process_item(result)

        self.response_number += 1

    def _error_callback(self, exception):
        try:
            raise exception
        except:
            logger.exception(exception)

    def _callback(self, temp):
        # 如果还需要继续执行，那么继续递归
        if self.running:
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback, error_callback=self._error_callback)

    def main(self):
        self.running = True
        start = datetime.now()
        logger.info('爬虫运行开始时间: %s' % start)
        '''
        提供程序运行的入口
        :return:
        '''
        self.pool.apply_async(self._execute_start_requests, error_callback=self._error_callback)

        for i in range(self.max_async):
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback, error_callback=self._error_callback)

        # 让主线程 阻塞
        while True:
            # 节省cpu消耗
            time.sleep(0.001)
            # self.pool.sleep(0.001)
            # self.pool.apply_async(self._execute_request_response_item, error_callback=self._error_callback)
            # 当满足条件
            if self.response_number == self.scheduler.request_number and self.scheduler.request_number != 0:
                self.running = False
                break

        # 保证主线程退出前，子线程全部执行完
        self.pool.close()
        self.pool.join()

        end = datetime.now()
        logger.info('爬虫运行结束时间: %s' % end)
        logger.info('共发起请求: %d'% self.response_number)
        logger.info('共耗时: {:.2f}s'.format((end-start).total_seconds()))

