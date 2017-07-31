"""The Spider for news of school websites"""

import scrapy
from spider.items import NewsItem
from spider.settings import NEWS_CONFIG

NAME_COLUMN = 0
URL_COLUMN = 1
PATTERN_COLUMN = 2


class NewsSpider(scrapy.Spider):
    """Spider Definition"""
    name = 'news'

    def start_requests(self):
        for config in NEWS_CONFIG:
            print('==================config===================')
            req = scrapy.Request(url=config[URL_COLUMN], callback=self.parse)
            req.meta['pattern'] = config[PATTERN_COLUMN]
            req.meta['name'] = config[NAME_COLUMN]
            yield req

    def parse(self, res):
        data_list = res.css(res.meta['pattern'])
        print('==================parse=============')
        print(res.meta['name'])
        for post in data_list:
            item = NewsItem()
            item['name'] = res.meta['name']
            item['title'] = post.css('a::text').extract_first().strip()
            item['href'] = post.css('a::attr(href)').extract_first().strip()
            item['time'] = post.css('span::text').extract_first().strip()
            yield item
