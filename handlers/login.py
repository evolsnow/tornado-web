'''
Created on Oct 29, 2015

@author: ev0l
'''
import tornado.gen

from handlers import BaseHandler


class LoginHandler(BaseHandler):
    '''
    登录函数, 数据库的写入, 设置安全cooike, 30天失效
    '''
    def get(self):
        self.error_render(None, "")

    @tornado.gen.coroutine
    def post(self):
        db_user = self.application.db.user
        pwd = yield db_user.find_one({"name": self.get_argument("name")})
        try:
            if tornado.escape.utf8(self.get_argument("password")) \
                    == pwd["password"]:
                self.set_secure_cookie("user", self.get_argument("name"))
                self.set_secure_cookie(
                                       "password", self.get_argument("password"))
                self.redirect(self.get_argument("next", "/"))

            else:
                self.error_render("密码错误", self.get_argument("name"))
        except:
            self.error_render("用户不存在", "")
            # self.redirect("/register")

    def error_render(self, warning, user):
        kwargs = dict(title="用户登录", head="请登录", user=user,
                      button_name="登录", action="login",
                      next=self.get_argument("next", "/"),
                      warning_message=warning)
        self.render("login_reg.html", **kwargs)

route = [(r"/login", LoginHandler), ]
