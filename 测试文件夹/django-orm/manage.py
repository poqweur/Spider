#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

import os, sys

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setting")  # 这里写你要连接的配置名

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)