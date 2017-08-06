# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import requests
import json

from .settings import SERVER_FETCH_URL


class MongoPipeline(object):
    collection_name = 'posts'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    def insert_post(self, post):
        if not self.is_dup(post):
            requests.post(SERVER_FETCH_URL, data={
                'post': json.dumps(post)
            })
            self.collection.insert_one(post)

    def is_dup(self, post):
        return self.collection.find_one(post) is not None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'BAK'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient('db')
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_name]

    def process_item(self, item, spider):
        self.insert_post(dict(item))
        return item
