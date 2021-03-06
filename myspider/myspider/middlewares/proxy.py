#-*-coding:utf-8-*-

import os
import random 
import logging

class RandomProxyMiddleware(object):
    proxys=[]
    
    def __init__(self):  
        fp =  os.path.dirname(os.getcwd())+'/middlewares/proxys.txt'
        try:
            logging.info("proxy path:%s"%fp)
            fl = open(fp,'r')
            
            try:
                lines = fl.readlines()
                for l in lines:
                    if l!="":
                        self.proxys.append(l)
            finally:
                fl.close()
        except Exception,ex:
            raise Exception("user agent error:%s"%ex)
            
    def process_request(self,request,spider): 
        proxy = random.choice(self.proxys)
        logging.info("proxy:%s"%proxy)
        if proxy:
            request.meta['proxy'] = "http://%s/"%proxy

