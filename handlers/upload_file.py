'''
Created on Oct 29, 2015

@author: ev0l
'''
import Image
import time
import tornado.gen

import StringIO
from handlers import BaseHandler
from handlers import new_pic_notify
from utils import mkdir


class UploadFileHandler(BaseHandler):
    '''图片上传handler,需要先登录'''
    @tornado.web.authenticated
    def get(self):
        self.render("upload.html")

    @tornado.web.authenticated
    def post(self):
        '''以时间戳+用户名方式存入数据库,防止同名覆盖'''
        f = self.request.files['file'][0]
        rawname = f['filename']
        suffix = f['filename'].split('.')[-1]
        name_part = self.get_secure_cookie("user")
        self.dstname = str(int(time.time())) + name_part + \
                '.' + rawname.split('.').pop()
        time_now = time.strftime('%Y_%m_%d', time.localtime(time.time()))
        self.path = "static/pic/" + time_now + "/"
        mkdir(self.path)
        if suffix.lower() in ('jpg', 'jpeg', 'gif', 'bmp', 'png'):
            img = Image.open(StringIO.StringIO(f['body']))
            img.save(self.path + self.dstname)
            self.save_to_db_pic(self.dstname, self.path)
            new_pic_notify.NewPicNotifyHandler.send_message("new")
        else:
            self.write("<script>alert('图片格式错误!')</script>")
        self.redirect("/")

    @tornado.gen.coroutine
    def save_to_db_pic(self, pic_name, pic_path):
        '''
        存入数据库,包含图片名字,路径,所有者
        后期图片评论和点赞数通过update方法写入
        '''
        db_pic = self.application.db.pic
        db_user = self.application.db.user
        owner = self.get_secure_cookie("user")
        owner_avatar = yield db_user.find_one({"name": owner})
        try:
            content_avatar = owner_avatar["avatar_path"] + \
                    owner_avatar["avatar_name"]
        except:
            content_avatar = "static/avatar/guest.png"
        dic = {"pic_name": pic_name, "pic_path": pic_path,
                "head_pic_url": content_avatar,
                "owner": owner}
        db_pic.insert(dic)

route = [(r"/upload", UploadFileHandler), ]
