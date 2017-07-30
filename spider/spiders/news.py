import scrapy
from spider.items import NewsItem
from spider.settings import NEWS_CONFIG

NAME_COLUMN = 0
URL_COLUMN = 1
PATTERN_COLUMN = 2

class NewsSpdier(scrapy.Spider):
  name = 'news'

  def start_requests(self):
    for config in NEWS_CONFIG:
      print('============config===========')
      print(config)
      self.pattern = config[PATTERN_COLUMN]
      yield scrapy.Request(url=config[URL_COLUMN], callback=self.parse)

  def parse(self, response):
    data_list = response.css(self.pattern)
    for post in data_list:
      item = NewsItem()
      item['title'] = post.css('a::text').extract_first().strip()
      item['href'] = post.css('a::attr(href)').extract_first().strip()
      item['time'] = post.css('span::text').extract_first().strip()
      yield item