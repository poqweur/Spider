#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: WangJY



from mini_scrapy.core.spiders import Spider, Request

class BaiduSpider(Spider):
    start_url = 'http://www.baidu.com'

    name = 'baidu'

    def parse(self, response):
        return response.url

'''
class DoubanTop(Spider):

    name = 'douban'

    def start_requests(self):
        base_url = 'https://movie.douban.com/top250?start={}'


        for i in range(0, 250, 25):
            url = base_url.format(i)
            yield Request(url, parse='parse')
            # yield Request(url, parse='parse')
            # yield Request(url, parse='parse')


    def parse(self, response):
        # print('parse', response.url)
        for li in response.xpath('//ol[@class="grid_view"]/li'):

            title = li.xpath('.//span[@class="title"][1]/text()')[0]
            yield title  # 数据

            link = li.xpath('.//div[@class="info"]/div[@class="hd"]/a/@href')
            yield Request(link[0], parse='parse_detail')

    def parse_detail(self, response):
        # print('response', response.url)
        pass
'''

class ToutiaoSearch(Spider):

    name = "toutiao"
    base_url = 'https://www.toutiao.com'

    headers = {
        "Accept": "application/json, text/javascript",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": 'UM_distinctid=15ec61597d5367-05eeab2649a34a-c303767-144000-15ec61597d8707; uuid="w:ffc8175ec65c48499b1885353b1792a7"; tt_webid=6470633900389795342; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=gr12qg6t11510716429942; CNZZDATA1259612802=1497104753-1506558970-%7C1510714329; tt_webid=6470633900389795342',
        "Host": "www.toutiao.com",
        # "Referer": "https://www.toutiao.com/search/?keyword=%E4%BC%A0%E6%99%BA",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    def start_requests(self):
        url = "https://www.toutiao.com/search_content/"
        params = {
            "offset": 0,
            "format": "json",
            "keyword": u"python",
            "autoload": "true",
            "count": "20",
            "cur_tab": "1",
        }

        for k in ['比特币', '人工智能', '区块链', '宪法修订']:
            params["keyword"] = k
            yield Request(url, parse="parse_list", headers=self.headers, params=params)

    def parse_list(self, response):
        data = response.json

        for item in data["data"]:
            if not item.get("article_url") or not item.get("media_name"):
                continue
            article_link = item["article_url"]
            title = item["title"]
            pub_date = item["datetime"]
            author = item["media_name"]
            try:
                author_link = item["media_url"]
            except:
                author_link = ''

            yield {
                "title": title,
                "article_link": article_link,
                "author": author,
                "author_link": author_link,
                "pub_date": pub_date,
                "keyword": response.request.params["keyword"],
                "source": u"今日头条"
            }

        if data["data"]:
            response.request.params["offset"] += 20
            yield response.request