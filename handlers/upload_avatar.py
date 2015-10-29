'''
Created on Oct 29, 2015

@author: ev0l
'''
import Image
import tornado.web

import StringIO
from handlers import BaseHandler


class UploadAvatar(BaseHandler):
    '''上传头像'''
    @tornado.web.authenticated
    def get(self):
        self.render("avatar.html")

    @tornado.web.authenticated
    def post(self):
        '''同一用户只有一个头像'''
        f = self.request.files['file'][0]
        suffix = f['filename'].split('.')[-1]
        self.user = self.get_secure_cookie("user")
        self.avatarname = self.user + '.' + suffix.lower()
        self.path = "static/avatar/"
        if suffix.lower() in ('jpg', 'jpeg', 'bum', 'png'):
            img = Image.open(StringIO.StringIO(f['body']))
            img.save(self.path + self.avatarname)
            self.save_to_db_user(self.avatarname, self.path, self.user)
        else:
            self.write("<script>alert('图片格式错误')</script>")
        self.redirect("/")

    @tornado.gen.coroutine
    def save_to_db_user(self, avatarname, path, user):
        db_user = self.application.db.user
        doc = yield db_user.find_one({"name": user})
        _id = doc['_id']
        dic = {"avatar_name": avatarname, "avatar_path": path}
        yield db_user.update({'_id': _id}, {'$set': dic})

route = [(r"/avatar", UploadAvatar), ]
