# -*- coding: utf-8 -*-

import scrapy
import logging 
import myspider.utils

class IPRSpider(scrapy.Spider):
    name = "IPRSpider"
    allowed_domains = ["pss-system.gov.cn"]
    headers={
        "Accept":"text/html, */*",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Connection":"keep-alive", 
        "Content-Type":"application/x-www-form-urlencoded",
        "Referer":"http://www.pss-system.gov.cn/sipopublicsearch/search/searchHomeIndex.shtml" 
    }
    
    def start_requests(self):  
        return [scrapy.FormRequest(url="http://www.pss-system.gov.cn/sipopublicsearch/search/executeTableSearchAC!originalCode1.do",formdata={
            "searchCondition.searchExp":u"公开（公告）日>=2000-01-01",
            "searchCondition.dbId":"VDB",
            "searchCondition.searchType":"Sino_foreign",
            "searchCondition.power":"false",
            "wee.bizlog.modulelevel":"0200201"
        },headers=self.headers,meta={'start':'0'},callback=self.parse_content)] 
                                   
    def mapToItem(self,response):
        details = []
        
        for block in response.xpath("//div[contains(@id,'result_record_main_div')]"):
            self.logger.info("======================================================")
            detail = {}
            for ele in block.xpath(".//div[contains(@id,'result_inner_left_div')]/div"):
                try:
                    item_name = ele.xpath(".//table/tr/td/strong/text()").extract_first()
                    item_text = ele.xpath(".//table/tr/td/text()").extract()  
                    
                    if item_name == None:
                        continue
                         
                    self.logger.info("name:%s text:%s",item_name.strip() if item_name!=None else "","".join(item_text.strip()) if item_text!=None else "")
                    detail[strips(item_name,['\n','\t',' '])] = strips("".join(item_text),['\n','\t',' '])
                except Exception,ex:
                    self.logger.error(ex)
                    
            for ele in block.xpath(".//div[contains(@id,'result_link_div')]/a"):
                try:
                    item_name = ele.xpath("text()").extract_first()
                    item_text = ele.xpath("@href").extract_first()
                     
                    self.logger.info("name:%s text:%s",item_name.strip() if item_name!=None else "","".join(item_text).strip() if item_text!=None else "")
                    detail[strips(item_name,['\n','\t',' '])] = strips("".join(item_text),['\n','\t',' '])
                except Exception,ex:
                    self.logger.error(ex)
                    
            details.append(detail)
        
        return details
                                        
    def parse_content(self,response,**kwargs):
        self.logger.info('A response from %s just arrived! status:%s pageindex:%s'%(response.url,response.status, response.meta['start']))  
       
        pageindex = int(response.meta['start'])
        next_page_index = str((pageindex if pageindex!=0 else 670) +10)
        
        item = {}
        
        item['index'] = pageindex
        item['url'] = response.url
        item['response_status'] = response.status
        item['html'] = response.body
        item['status']=0
        
        yield item
     
        yield scrapy.FormRequest(url='http://www.pss-system.gov.cn/sipopublicsearch/search/showSearchResult-startWa.shtml',
                                 formdata={
                                        "resultPagination.limit":"10",
                                        "resultPagination.sumLimit":"10",
                                        "resultPagination.start":next_page_index,
                                        "resultPagination.totalCount":"78496625",
                                        "searchCondition.searchType":"Sino_foreign",
                                        "searchCondition.dbId":"",
                                        "searchCondition.power":"false",
                                        "searchCondition.strategy":"",
                                        "searchCondition.literatureSF":"",
                                        "searchCondition.searchExp":u"公开（公告）日>=2001-01-01",
                                        "searchCondition.executableSearchExp":"VDB:(PD>='2001-01-01')",
                                        "wee.bizlog.modulelevel":"0200201",
                                        "searchCondition.searchKeywords":"",
                                        "searchCondition.searchKeywords":"[2][ ]{0,}[0][ ]{0,}[0][ ]{0,}[1][ ]{0,}[.][ ]{0,}[0][ ]{0,}[1][ ]{0,}[.][ ]{0,}[0][ ]{0,}[1][ ]{0,}"
                                    },
                                    headers = self.headers,
                                    meta = {'start':next_page_index},
                                    callback = self.parse_content)
                    
                    
