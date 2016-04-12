# -*- coding: utf-8 -*-
import scrapy 
import urlparse
import re   
from myspider.mongo import mongoDbContext  

class SinagbSpider(scrapy.Spider):
    name = "SinagbSpider"
    allowed_domains = ["sina.com","sina.com.cn"]
    start_urls = (
        'http://guba.sina.com.cn/?s=bar&bid=14247',
    )
    
    rules=[{ 
            'url':'http://guba.sina.com.cn/\?s=bar&bid=\d+',
            'rule':{
                'baseUrl':'http://guba.sina.com.cn',
                'urlMatch':'div.table_content table td a[class*=linkblack]',
                'fieldPath':'div.table_content table td a[class*=linkblack]', 
                'fields':{
                    'title':'text()'
                }, 
                'next_page':u'//a[text()="下一页"]/@href'
            }
          },
          { 
            'url':'http://guba.sina.com.cn/\?s=thread&tid=\d+&bid=\d+',
            'rule':{
                'baseUrl':'',
                'urlMatch':'',
                'fieldPath':'div#thread div.il_txt', 
                'fields':{
                    'title':'//h4/text()',
                    'content':'//div[id="thread_content"]/text()'
                }, 
                'next_page':u''
            }
          }]
          
    ignore_urls=[]
    
    def mapToItem(self,response,rule,ele):
        item={'fromUrl':response.url,'status':response.status,'columns':{}} 
        
        fields=rule['fields']
        for k in fields.keys(): 
            value = ele.xpath(fields[k]).extract()
            item['columns'][k] = value
        
        return item
    
    def parse(self, response): 
        for rule in self.rules:   
            if re.match(rule['url'],response.url):
                baseUrl=rule['rule']['baseUrl']
                
                for ele in response.css(rule['rule']['fieldPath']):
                    yield self.mapToItem(response, rule['rule'], ele)
                
                if rule['rule']['urlMatch']!='':
                    for url in response.css(rule['rule']['urlMatch']).xpath('@href'):   
                        yield scrapy.Request(baseUrl+url.extract(), callback=self.parse) 
                
                if rule['rule']['next_page']!='':
                    for nextUrl in response.xpath(rule['rule']['next_page']):
                        self.log('next_page:'+nextUrl.extract())
                        yield scrapy.Request(baseUrl+nextUrl.extract(), callback=self.parse)
                    
     
     
