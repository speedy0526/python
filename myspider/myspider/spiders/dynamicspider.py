# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy.spiders import CrawlSpider,Rule 
from scrapy.linkextractors import LinkExtractor

import logging 
from myspider.mongo import mongoDbContext  

class MySpider(CrawlSpider):
    name = "MySpider"
     
    def __init__(self,*args, **kwargs):
        logging.warning("spider initizating.")
        
        rule = kwargs["rule"]
          
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allowed_domains
        self.allowed_urls = rule.allowed_url
        self.start_urls = rule.start_urls
        self.next_page = rule.next_page
        self.rules = self.parse_rules(rule)
        
        logging.warning(self.allowed_domains)
        logging.warning(self.start_urls)
        logging.warning("spider init complete.") 
        
        super(MySpider,self).__init__(self,*args,**kwargs)
        
        
    def parse_rules(self,rule):
        _rule_list = []

        if rule.next_page and rule.next_page !='':
            _next_page_extractorRule = Rule(LinkExtractor(restrict_xpaths = rule.next_page))
            _rule_list.append(_next_page_extractorRule)
            
        _content_extractorRule = Rule(LinkExtractor(allow = self.allowed_urls),callback = 'parse_item')
                                       
        _rule_list.append(_content_extractorRule)

        return tuple(_rule_list)

        
    def parse_item(self,response):
        logger.warning(response.url)
        item={'fromUrl':response.url,'status':response.status}  
        
        if self.rule.snapshot == True:
            item["snapshot"] = response.read()
            
        fields = self.rule.content
        for k in fields.keys(): 
            if self.rule.findMode=="xpath":
                value = response.xpath(fields[k]).extract()
            else :
                value = response.css(fields[k]).extract()
                    
            item[k] = value

        return item
        
