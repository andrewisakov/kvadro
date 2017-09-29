#!/usr/bin/python3
import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import uuid
import json
import pprint
from tornado.escape import json_decode
from tornado.escape import json_encode
from tornado.options import define, options
import handlers


define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        routes = [
            (r"/", handlers.MainHandler),
            (r"/api/uploadtext/", handlers.AjaxHandler),
            (r"/api/gettext/", handlers.AjaxHandler),
            (r"/api/deleterows/", handlers.AjaxHandler),
        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )
        tornado.web.Application.__init__(self, routes, **settings)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
