# -*- coding: utf-8 -*-

import sqlite3

class SqliteDbContext(object):
    def __init__(self):
        self.db = sqlite3.connect("scrapy.db3")
        #self.initDb()
        
    def initDb(self):
        self.db.execute('CREATE TABLE spiders (id INTEGER PRIMARY KEY, name TEXT, start_urls TEXT, allow_domains TEXT, status NUMERIC, descrpition text)')
        self.db.execute('CREATE TABLE rules (id INTEGER PRIMARY KEY, spiderid NUMERIC, allow TEXT, deny TEXT, restrict_xpath TEXT,restrict_css TEXT , fllow bool, allow_domains text, deny_domains text)')
        self.db.execute('insert into spiders(name,start_urls,allow_domains,status,descrpition) values   ("sinaSpider","sina.com,sina.com.cn","sina.com,sina.com.cn",1,"")')
        self.db.execute('insert into rules(spiderid,allow,deny,restrict_xpath,restrict_css,fllow,allow_domains,deny_domains) values(1,"doc-\w+.shtml","","","",1,"","")')
        
    def execute(self,sql):
        return self.db.execute(sql)

    def commit(self):
        self.db.commit()
