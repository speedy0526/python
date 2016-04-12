# -*- coding: utf-8 -*-
import scrapy 
import urlparse
from myspider.mongo import mongoDbContext 
from myspider.items import PostItem
import re
import urllib 

class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["sina.com","sina.com.cn"]
    start_urls = (
        'http://guba.sina.com.cn/?s=bar&bid=14247',
    )
    
    rules=[{ 
            'url':'http://guba.sina.com.cn/\?s=bar&(bid=\d+|name=\S+)',
            'rule':{
                'baseUrl':'http://guba.sina.com.cn',
                'urlMatch':'div.table_content table td a[class*=linkblack]',
                'fieldPath':'div.table_content table td a[class*=linkblack]', 
                'fields':{
                    'title':'text()',
                    'url':'@href'
                }, 
                'next_page':u'//a[text()="下一页"]/@href'
            }
          }]
          
    
    def mapToItem(self,response,rule,ele):
        item={'fromUrl':response.url,'status':response.status}  
         
        fields=rule['fields']
        for k in fields.keys(): 
            value = ele.xpath(fields[k]).extract()
            item[k] = value
        
        return item
    
    def parse(self, response): 
        for rule in self.rules:   
            if re.match(rule['url'],response.url):
                baseUrl=rule['rule']['baseUrl']
                 
                for ele in response.css(rule['rule']['fieldPath']):  
                    yield self.mapToItem(response, rule['rule'], ele)
                
                if rule['rule']['next_page']!='':  
                    for p in response.xpath(rule['rule']['next_page']).extract(): 
                        self.log('new next page:'+ p.encode('gb2312'))
                        yield scrapy.Request(baseUrl + p.encode('gb2312'), callback=self.parse)
                    
     
     
