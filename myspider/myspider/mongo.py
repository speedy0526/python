# -*- coding: utf-8 -*-

import pymongo

class mongoDbContext:
    def __init__(self):
        self._conn = pymongo.MongoClient('127.0.0.1',27017)
        self.db = self._conn['IPRDB']

    def add(self,name,data):
        self.db[name].insert_one(data)

    def find(self,name,filter):
        return self.db[name].find()
        
    def findOne(self,name,fileter):
        return self.db[name].find_one(filter)
        
    def count(self,name):
        return self.db[name].count()
