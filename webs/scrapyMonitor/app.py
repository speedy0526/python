import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web 
from tornado.options import define, options
from routes import Application
import home
import os

define("port", default=8000, help="run on the given port", type=int)
 
if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application(static_path=os.path.join(os.path.dirname(__file__).decode('utf-8','ignore'), "static"))
    app.load_handler_module(home)
    #app = tornado.web.Application(handlers=[(r'/', home.IndexRequestHander)],template_path=os.path.join(os.path.dirname(__file__), "views"))
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()
