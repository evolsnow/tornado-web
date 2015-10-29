'''
Created on Oct 29, 2015

@author: ev0l
'''
import tornado.web
import uuid

from handlers import BaseHandler


class NewPicNotifyHandler(BaseHandler):
    '''
    新上传图片顶部推送通知，基于AJAX长连接。
    '''
    callbacks = set()
    users = set()

    @tornado.web.asynchronous
    def get(self):
        self.callbacks.add(self.on_new_message)
        self.user = self.get_cookie("user")
        if not self.user:
            self.user = str(uuid.uuid4())
            self.set_cookie("user", self.user)
        if self.user not in self.users:
            self.users.add(self.user)

    def on_new_message(self, message):
        if self.request.connection.stream.closed():
            return
        self.write(message)
        self.finish()

    def on_connection_close(self):
        self.callbacks.remove(self.on_new_message)
        self.users.discard(self.user)

    @classmethod
    def send_message(cls, message):
        for callback in cls.callbacks:
            try:
                callback(message)
            finally:
                cls.callbacks = set()

route = [(r"/ajax", NewPicNotifyHandler), ]
