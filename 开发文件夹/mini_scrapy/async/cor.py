#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

import gevent
from gevent import monkey
monkey.patch_all()

from gevent.pool import Pool as BasePool


class Pool(BasePool):

    def apply_async(self, func, args=None, kwds=None, callback=None, error_callback=None):
        super().apply_async(func, args=args, kwds=kwds, callback=callback)

    def close(self):
        pass

    def sleep(self, n):
        gevent.sleep(n)