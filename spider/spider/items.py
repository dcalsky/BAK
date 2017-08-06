import scrapy


class NewsItem(scrapy.Item):
    name = scrapy.Field()
    cname = scrapy.Field()  # Chinese name
    title = scrapy.Field()
    href = scrapy.Field()
    time = scrapy.Field()
    # when = scrapy.Field()
