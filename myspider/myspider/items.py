# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class PostItem(Item):
    title=Field()
    content=Field()
    url=Field()
    user=Item()
    fromurl=Field()
    postdate=Field() 
 
class UserItem(Item):
    userid=Field()
    nickname=Field()
    gender=Field()
    avatar=Field()
    location=Field()
    introduce=Field()
    
    
    
#def dynamic(name,fields):
#    fieldlist={fname:Field() for fname in fields}
#    return typeof(name,(DictItem,),{'fields':fieldlist})
