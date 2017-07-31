import scrapy


class NewsItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    time = scrapy.Field()
