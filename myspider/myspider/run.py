# -*- coding: utf-8 -*-

import logging
from scrapy.crawler import CrawlerRunner,Crawler
from twisted.internet import reactor, defer 
from scrapy.utils.project import get_project_settings
from scrapy.spiders import Rule 
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.log import configure_logging
import sys
sys.path.append(u"/home/leo/桌面/python/myspider".encode('utf-8','ignore'))

from myspider.spiders.broadspider import BroadSpider
from myspider.sqlitedb import SqliteDbContext

class Runner(object):
    def __init__(self,*args,**kwargs): 
        configure_logging()
        self.settings = get_project_settings()
        self.runner = CrawlerRunner(self.settings) 

    def add(self,*a,**kw):  
        crawler = Crawler(BroadSpider,self.settings) 
        self.runner.crawl(crawler,*a,**kw)

    def start(self): 
        d = self.runner.join()
        d.addBoth(lambda _: reactor.stop()) 
        reactor.run()

    def stop(self):
        self.runner.stop()
        reactor.stop()
         
runner = Runner()  

try:
    db = SqliteDbContext()
    sc = db.execute("SELECT id,name,start_urls,allow_domains,status FROM spiders")
    for row in sc:  
        name = row[1]
        start_urls = row[2].split(",") 
        allow_domains = row[3].split(",") if row[3] != None and row[3] != "" else []

        rules = [] 
        rl = db.execute("select * from rules where spiderid=%s" % row[0])
        for r in rl:
            extractor = LinkExtractor(allow=tuple(r[2].split(",")),
                                        deny=tuple(r[3].split(",")) if r[7] != None and r[3]!="" else (),
                                        restrict_xpaths=tuple(r[4].split(",")) if r[7] != None and r[4]!="" else (),
                                        restrict_css=tuple(r[5].split(",")) if r[7] != None and r[5]!="" else (),
                                        allow_domains=tuple(r[7].split(",")) if r[7] != None and r[7]!="" else (),
                                        deny_domains=tuple(r[8].split(",")) if r[8] != None and r[8]!="" else ())  

            rules.append(Rule(extractor,callback="parse_item", cb_kwargs={"content":{ "title":"","body":"" }}, follow=bool(r[6])))
             
        runner.add(name=name,
                   start_urls=start_urls,
                   allow_domains=allow_domains,
                   rules = rules)
except Exception:
    raise
    
runner.start()


