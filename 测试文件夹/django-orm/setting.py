#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY



SECRET_KEY = '123'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysql',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}