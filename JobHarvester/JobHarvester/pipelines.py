# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class JobharvesterPipeline:
    def process_item(self, item, spider):
        return item


class MongoPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = self.get_collection_name(spider)
        if self.db[collection_name].find_one({'item_id': item['item_id']}):
            spider.logger.info(f"Item with id {item['item_id']} already exists.")
        else:
            self.db[collection_name].insert_one(dict(item))
            spider.logger.info(f"Item with id {item['item_id']} added to MongoDB.")
        return item

    def get_collection_name(self, spider):

        if spider.preset == 1:
            collection_name = f"{spider.experience_level}_{spider.universal_category}_collection"
        elif spider.preset == 2:
            collection_name = f"{spider.experience_level}_{spider.universal_category}_collection"
        else:
            collection_name = 'unknown'

        collection_name = collection_name.lower().replace(" ", "_").replace(",", "_")
        return collection_name
