#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

from django.db import models

class user(models):

    name = models.CharField(max_length=20, verbose_name='名字')