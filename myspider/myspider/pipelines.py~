# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from myspider.mongo import mongoDbContext
from scrapy.exceptions import DropItem

class MyspiderPipeline(object):
    def __init__(self):
        self.db = mongoDbContext()
        
    def process_item(self, item, spider): 
        self.db.add('IPRData',item)
        return item 
        
        

