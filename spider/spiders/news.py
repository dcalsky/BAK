"""The Spider for news of school websites"""

import scrapy
from spider.items import NewsItem
from spider.settings import NEWS_CONFIG
from datetime import datetime

NAME_COLUMN = 0
URL_COLUMN = 1
PATTERN_COLUMN = 2


class NewsSpider(scrapy.Spider):
    """Spider Definition"""
    name = 'news'

    def start_requests(self):
        for config in NEWS_CONFIG:
            yield scrapy.Request(
                url=config[URL_COLUMN],
                callback=self.parse,
                meta={
                    'pattern': config[PATTERN_COLUMN],
                    'name': config[NAME_COLUMN]
                })

    # TODO: Sub-cells of post need to be parsed more flexible
    def parse(self, res):
        data_list = res.css(res.meta['pattern'])
        for post in data_list:
            yield NewsItem(
                name=res.meta['name'],
                title=post.css('a::text').extract_first().strip(),
                href=post.css('a::attr(href)').extract_first().strip(),
                time=post.css('span::text').extract_first().strip(),
                # when=datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            )
