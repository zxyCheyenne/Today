#!/usr/bin/env python
#
# Copyright 2016 Ours
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import MySQLdb
import os.path
import torndb
import re
import subprocess
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# my py file
from myHandlers.HomeHandler import HomeHandler
from myHandlers.AuthHandlers import *
from myHandlers.PostHandlers import PublishHandler,EntryHandler,CommentHandler
from myHandlers.ProfileHandler import *
from myHandlers.Relation import FollowHandler,UnFollowHandler,\
                                MyFollowerHandler, MyFollowHandler
from myHandlers.Paginator import Paginator
from myHandlers.SearchHandlers import SearchHandler


from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="today", help="blog database name")
define("mysql_user", default="today", help="blog database user")
define("mysql_password", default="today", help="blog database password")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/auth/signup", AuthSignupHandler),
            (r"/auth/signin", AuthSigninHandler),
            (r"/auth/signout", AuthSignoutHandler),
            (r"/newPost", PublishHandler),
            (r"/detail/([^/]+)", EntryHandler),
            (r"/comment/([^/]+)", CommentHandler),
            (r"/profile/([^/]+)", ProfileHandler),
            (r"/edit/profile", ProfileEditHandler),
            (r"/follow/([^/]+)", FollowHandler),
            (r"/unfollow/([^/]+)", UnFollowHandler),
            (r"/myfollower", MyFollowerHandler),
            (r"/myfollow", MyFollowHandler),
            (r"/myProfile", MyProfileHandler),
            (r"/search/", SearchHandler),
        ]
        settings = dict(
            app_title=u"TODAY",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Entry": EntryModule, "Paginator":Paginator},
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/signin",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

        self.maybe_create_tables()


    def maybe_create_tables(self):
        try:
            self.db.get("SELECT COUNT(*) from entries;")
        except MySQLdb.ProgrammingError:
            subprocess.check_call(['mysql',
                                   '--host=' + options.mysql_host,
                                   '--database=' + options.mysql_database,
                                   '--user=' + options.mysql_user,
                                   '--password=' + options.mysql_password],
                                  stdin=open('schema.sql'))

class EntryModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string("modules/entry.html", entry=entry)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
