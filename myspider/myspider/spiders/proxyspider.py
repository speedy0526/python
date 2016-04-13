# -*- coding: utf-8 -*-
import scrapy
class ProxySpilder(scrapy.Spider):
    name="ProxySpilder"
    start_urls=['http://www.xicidaili.com/']
    
    def parse(self,response,**kwargs):
        pass
