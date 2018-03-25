#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

import logging
import time
import threading
from multiprocessing.dummy import Pool  # 线程池
# from multiprocessing import Pool  # 进程池


def func():
    print(threading.current_thread().name)
    time.sleep(0.5)
    print('func')
    # raise Exception('123')
    return 'ok'

def func2():
    time.sleep(0.3)
    print('func2')

def func3():
    time.sleep(0.1)
    print('func3')

def func4():
    time.sleep(0)
    print('func4')

p = Pool(5)
# 同步执行
# p.apply(func)
# p.apply(func2)
# p.apply(func3)
# p.apply(func4)
# p.close()
# p.join()

def callback(temp):
    print(threading.current_thread().name)
    print(temp)

def error_callback(temp):
    print(threading.current_thread().name)
    try:
        raise temp
    except:
        logging.exception(temp)


print(threading.current_thread().name)
# 异步执行
p.apply_async(func, callback=callback, error_callback=error_callback)
p.apply_async(func, callback=callback, error_callback=error_callback)
p.apply_async(func, callback=callback, error_callback=error_callback)
p.apply_async(func, callback=callback, error_callback=error_callback)

# p.apply_async(func2)
# p.apply_async(func3)
# p.apply_async(func4)
while True:
    time.sleep(0.0001)

p.close()
p.join()