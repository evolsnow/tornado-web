# !-*-coding:utf-8-*-

import os
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options
import tornado.options
import tornado.web

import motor
from ui_modules import picture


define("port", default=8000, help="run on the given port", type=int)
define("loadnum", default=10, help="pic number to load adt once", type=int)

class Application(tornado.web.Application):                        
    def __init__(self):
        from urls import routes as handlers        
        settings = dict(
                cookie_secret=
                "19N9ViOvRmmikCmFiW4ZBYgo17MZ6k+auNmdk+Aa18I=",
                login_url="/login",
                xsrf_cookies=True,
                debug=True,
                template_path=os.path.join(os.path.dirname(__file__),
                    "templates"),
                static_path=os.path.join(os.path.dirname(__file__),
                    "static"),
                ui_modules={"Picture": picture.PictureModule}
                )
        self.db = motor.MotorClient().info
        self.loadnum = options.loadnum
        self.port = options.port
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
