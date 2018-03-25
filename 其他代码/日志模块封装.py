#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

import logging


# 日志的等级
# logging.DEBUG    # 1
# logging.INFO    # 2
# logging.WARNING    # 3
# logging.ERROR    # 4
# logging.CRITICAL    # 5
#
#
# logging.basicConfig(level=logging.INFO)
#
# logging.debug("debug")
# logging.info("info")
# logging.warning("warning")
# logging.error("error")
# logging.critical("critical")


class Logger(object):

    def __init__(self,
                 level=logging.INFO,
                 filename='log.log',
                 format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                 datefmt='%Y-%m-%d %H:%M:%S'
        ):
        # 1. 获取一个logger对象
        self._logger = logging.getLogger("test_log")

        # 指定logger输出格式
        self.formatter = logging.Formatter(
            fmt=format,
            datefmt=datefmt
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
        file_handler.setFormatter(self.formatter)  # 可以通过setFormatter指定输出格式
        return file_handler

    def get_console_handler(self):
        # 控制台日志
        console_handler = logging.StreamHandler()
        console_handler.formatter = self.formatter  # 也可以直接给formatter赋值
        return console_handler

    @property
    def logger(self):
        return self._logger


logger = Logger(level=logging.DEBUG).logger

logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.critical("critical")