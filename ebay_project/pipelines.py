import pymongo
import sys
import logging
from .items import EbayProjectItem
from itemadapter import ItemAdapter
class MongoDBPipeline(object):
    collection = 'faheem'
    
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri= mongo_uri
        self.mongo_db=mongo_db
    @classmethod
    def from_crawler(cls, crawler):
        
        return cls (
            mongo_uri= crawler.settings.get("MONGODB_SERVER"),
            mongo_db= crawler.settings.get("MONGODB_DB")
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[self.collection].delete_many({})

    def close_spider(self,spider):
        self.client.close()
        
    def process_item(self,item, spider):
        self.db[self.collection].insert_one(dict(item))
        logging.debug("Post added to MongoDB!")
        return item
# class MongoDBPipeline:

#     collection = 'scrapy_items'

#     def __init__(self, mongodb_uri, mongodb_db):
#         self.mongodb_uri = mongodb_uri
#         self.mongodb_db = mongodb_db
#         if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongodb_uri=crawler.settings.get('MONGODB_URI'),
#             mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
#         )

#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongodb_uri)
#         self.db = self.client[self.mongodb_db]
#         # Start with a clean database
#         self.db[self.collection].delete_many({})

#     def close_spider(self, spider):
#         self.client.close()

#     def process_item(self, item, spider):
#         data = dict(EbayProjectItem(item))
#         self.db[self.collection].insert_one(data)
#         return item