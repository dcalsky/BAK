# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import requests
import json

from .settings import SERVER_FETCH_URL, DB_HOST, DB_NAME, GATHER_MODE


class MongoPipeline(object):
    collection_name = 'posts'
    client = pymongo.MongoClient(DB_HOST)
    db = client[DB_NAME]
    collection = db[collection_name]

    def insert_post(self, post):
        if not self.is_dup(post):
            self.collection.insert_one(post)
            if not GATHER_MODE:
                # Once GATHER_MODE is open, spider will not send modified data to server
                requests.post(SERVER_FETCH_URL, data={
                    'post': json.dumps(post)
                })

    def is_dup(self, post):
        return self.collection.find_one(post) is not None

    def process_item(self, item, spider):
        self.insert_post(dict(item))
        return item
