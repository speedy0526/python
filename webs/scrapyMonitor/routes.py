#!/usr/bin/env python
# coding:utf-8
import os
import tornado.web
 
class Application(tornado.web.Application):  

    def load_handler_module(self, handler_module, perfix=".*$"): 
        is_handler = lambda cls: isinstance(cls, type) and issubclass(cls, RequestHandler)  
        has_pattern = lambda cls: hasattr(cls, 'url_pattern') and cls.url_pattern

        handlers = [] 
        for i in dir(handler_module):
            cls = getattr(handler_module, i)
            if is_handler(cls) and has_pattern(cls):
                handlers.append((cls.url_pattern, cls))

        self.add_handlers(perfix, handlers)
 
    def _get_host_handlers(self, request): 
        host = request.host.lower().split(':')[0] 
        handlers = (i for p, h in self.handlers for i in h if p.match(host)) 

        if not handlers and "X-Real-Ip" not in request.headers:
            handlers = [i for p, h in self.handlers for i in h if p.match(self.default_host)]

        return handlers
 
class RequestHandler(tornado.web.RequestHandler):
    url_pattern = None  
    template_path = ""

    def render(self, template_name, **kwargs):
        return super(RequestHandler,self).render(self.template_path + template_name, **kwargs)
 
def route(url_pattern,template_path=""): 
    def handler_wapper(cls): 
        cls.url_pattern = url_pattern

        if template_path != "":
            cls.template_path = template_path

        return cls

    return handler_wapper

