'''
Created on Oct 29, 2015

@author: ev0l
'''
import tornado.gen

from handlers import BaseHandler


class RegHandler(BaseHandler):
    '''
    注册界面, 基本数据库的增,查,写
    '''
    def get(self):
        self.error_render("")

    @tornado.gen.coroutine
    def post(self):
        db_user = self.application.db.user
        if  (yield db_user.find_one({"name": self.get_argument("name")})):
            self.error_render("用户名已注册")
        else:
            yield db_user.insert({"name": self.get_argument("name"),
                                  "password": self.get_argument("password")})
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect("/")

    def error_render(self, warning):
        kwargs = dict(title="用户注册", head="请注册",
                      button_name="注册", action="register",
                      next=self.get_argument("next", "/"),
                      warning_message=warning, user="")
        self.render("login_reg.html", **kwargs)

route = [(r"/register", RegHandler), ]
