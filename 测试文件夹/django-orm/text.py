#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

import django

from django.conf import settings
import setting as s



settings.configure(DATABASES=s.DATABASES, INSTALLED_APPS=['app'], DEBUG=True)
django.setup()