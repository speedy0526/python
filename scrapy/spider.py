#coding=utf-8
import scrapy
from scrapy.item import Item,Field
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor as lnk

import re
import json

class PostItem(Item):
    artical_name=Field()
    artical_url=Field()
 
 
class SinaFinancialSpider(CrawlSpider):
    name='SinaFinancial'
    allowed_domains=['sina.com.cn']
    start_urls=['http://guba.sina.com.cn/?s=bar&bid=14247']

    rules=[Rule(lnk(restrict_xpaths=('/div[@class="table_content"]/table/tbody/tr/td/a'),unique=True),
                callback='parse_item')]


    def parse_item(self,response): 
        print response.url
        

    def parser_content(self,content):
        pass
    
 
