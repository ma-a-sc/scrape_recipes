# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class ScrapeCookBooksDotComPipeline:

    def open_spider(self, spider):
        ...

    def close_spider(self, spider):
        ...

    def process_item(self, item, spider):
        return item
