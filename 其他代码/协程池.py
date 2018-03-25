#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY


from gevent.pool import  Pool


def func():
    print('func')
    raise Exception('ok')


class Gpool(Pool):

    def apply_async(self, func, args=None, kwds=None, callback=None, error_callback=None):
        super().apply_async(func, args=None, kwds=None, callback=None)

    def cloase(self):
        pass


p = Gpool()
p.apply_async(func, error_callback='asdasd')
p.apply_async(func)
p.apply_async(func)
p.apply_async(func)
p.apply_async(func)
p.join()