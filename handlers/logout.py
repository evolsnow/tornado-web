'''
Created on Oct 29, 2015

@author: ev0l
'''
from handlers import BaseHandler


class LogOutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")

route = [(r"/logout", LogOutHandler), ]
