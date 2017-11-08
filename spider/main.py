
# from twisted.internet import reactor
# import scrapy
from time import sleep
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from spider.spiders.news import NewsSpider

# configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})


# while(1):
#   runner = CrawlerRunner()
#   d = runner.crawl(NewsSpider)
#   d.addBoth(lambda _: reactor.stop())
#   reactor.run() # the script will block here until the crawling is finished
#   sleep(10)


import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spider.spiders.news import NewsSpider
process = CrawlerProcess(get_project_settings())
process.crawl(NewsSpider)
process.start()
