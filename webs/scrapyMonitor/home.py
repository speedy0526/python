import routes
from routes import route

@route("/","views/")
class IndexRequestHander(routes.RequestHandler):
    def get(self):
        self.render("index.html")
    
    def post(self):
        pass
        
@route("/","views/")      
class SpiderRequestHandler(routes.RequestHandler):
    def get(self):
        pass
        
    def post(self):
        pass
