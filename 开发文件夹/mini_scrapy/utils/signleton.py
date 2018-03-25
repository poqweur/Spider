#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY


def singleton(cls):
    instance = {}
    def _singleton(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return _singleton