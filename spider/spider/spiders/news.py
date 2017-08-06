"""The Spider for news of school websites"""

import scrapy
from spider.items import NewsItem
from spider.settings import NEWS_CONFIG
from datetime import datetime

DEFAULT_TITLE_PATTERN = 'a::text'
DEFAULT_HREF_PATTERN = 'a::attr(href)'
DEFAULT_TIME_PATTERN = 'span::text'

class NewsSpider(scrapy.Spider):
    """Spider Definition"""
    name = 'news'
    
    def start_requests(self):
        for site in NEWS_CONFIG['sites']:
            yield scrapy.Request(
                url=site['url'],
                callback=self.parse,
                meta=site)

    # TODO: Sub-cells of post need to be parsed more flexible
    def parse(self, res):
        site = res.meta
        post_list = res.css(site['post'])
        for post in post_list:
            yield NewsItem(
                name=site['name'],
                title=post.css(site['title'] or DEFAULT_TITLE_PATTERN).extract_first().strip(),
                href=post.css(site['href'] or DEFAULT_HREF_PATTERN).extract_first().strip(),
                time=post.css(site['time'] or DEFAULT_TIME_PATTERN).extract_first().strip(),
                # when=datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            )
