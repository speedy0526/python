# -*- coding: utf-8 -*-
import routes
from routes import route

@route("/","views")
class IndexRequestHander(routes.RequestHandler):
    def get(self):
        self.render("index.html")
    
    def post(self):
        pass
        
@route("/spider","views/spider/")      
class SpiderRequestHandler(routes.RequestHandler):
    def get(self):
        self.render("index.html")
        
    def post(self):
        pass
