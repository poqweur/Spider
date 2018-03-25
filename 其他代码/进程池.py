#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

import logging
from multiprocessing import Pool
from multiprocessing import Process,Manager


class Test():

    def __init__(self):
        self.pool = Pool()

    def task(self):
        print('func')

    def _err(self, ex):
        try:
            raise ex
        except:
            logging.exception(ex)

    def main(self):
        self.pool.apply_async(self.task, error_callback=self._err)
        # self.pool.apply_async(self.task)
        # self.pool.apply_async(self.task)
        # self.pool.apply_async(self.task)
        self.pool.close()
        self.pool.join()


t = Test()
t.main()
