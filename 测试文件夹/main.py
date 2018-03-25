#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY

from mini_scrapy.core.engine import Engine

from spiders import *
from middleware import *

spiders = {
    # DoubanTop.name: DoubanTop(),
    # BaiduSpider.name: BaiduSpider()
    ToutiaoSearch.name: ToutiaoSearch()
}

engine = Engine(spiders=spiders, spider_mids=[SpiderMiddleware()], downloader_mids=[DownloaderMiddleware()])
engine.main()


from multiprocessing import Process


# 多进程 + 线程
# 对进城 + 协程
# p = Process(target=engine.main)
# p2 = Process(target=engine.main)
# p.start()
# p2.start()
# p.join()
# p2.join()