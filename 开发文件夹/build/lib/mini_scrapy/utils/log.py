#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

import time
import logging

from mini_scrapy.conf.settings import LOG_CONFIG

from .signleton import singleton  # 单例

# logging.basicConfig(level=logging.INFO)
# # 日志等级
# logging.debug('debug')
# logging.info('info')
# logging.warning('warning')
# logging.error('error')
# logging.critical('critical')

@singleton
class Logger(object):

    def __init__(self,
                 level=LOG_CONFIG['level'],
                 filename=time.strftime('%Y-%m-%d',time.localtime(time.time())) + '.log',  # LOG_CONFIG['filename']
                 format=LOG_CONFIG['format'],
                 datafmt=LOG_CONFIG['datafmt']
                 ):
        # 1. 获取一个logger对象
        self._logger = logging.getLogger('test_log')

        # 指定logger输出格式
        self.fomatter = logging.Formatter(
            fmt=format,
            datefmt=datafmt
        )

        # 2. 为logger添加的日志处理器，分别是文件和命令行的
        self._logger.addHandler(self.get_file_handler(filename))
        self._logger.addHandler(self.get_console_handler())

        # 指定日志的最低输出级别，默认为WARN级别
        self._logger.setLevel(level)

    # 输出不同级别的log
    def get_file_handler(self, filename):
        # 文件日志
        file_handler = logging.FileHandler(filename)
        file_handler.setFormatter(self.fomatter)  # 可以通过setFormatter指定输出格式
        return file_handler

    def get_console_handler(self):
        # 控制台日志
        console_handler = logging.StreamHandler()
        console_handler.formatter = self.fomatter  # 也可以直接给formatter赋值
        return console_handler

    @property
    def logger(self):
        return self._logger


logger = Logger().logger

