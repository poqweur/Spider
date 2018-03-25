#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

import logging

LOG_CONFIG = {
    'level': logging.INFO,
    'filename': 'log.log',
    'format': '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
    'datafmt': '%Y-%m-%d %H-%M-%S'
}

MAX_ASYNC = 20