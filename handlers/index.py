'''
Created on Oct 29, 2015

@author: ev0l
'''
import tornado.gen

from handlers import BaseHandler


class MainHandler(BaseHandler):
    '''
    异步从数据库中读取图片路径, 初始加载的数目自定
    追踪用户点击加载更多的次数
    '''
    @tornado.gen.coroutine
    def get(self):
        db_pic = self.application.db.pic
        db_user = self.application.db.user
        loadnum = self.application.loadnum
        cursor = db_pic.find().sort([('_id', -1)]).limit(loadnum)
        self.piclist = []
        while (yield cursor.fetch_next):
            pic = cursor.next_object()
            owner_avatar = yield db_user.find_one({"name": pic["owner"]})
            try:
                comment = pic["comment"]
            except:
                comment = None
            try:
                content_avatar = owner_avatar["avatar_path"] + \
                        owner_avatar["avatar_name"]
            except:
                content_avatar = "static/avatar/guest.png"
            src = {"picurl": pic["pic_path"] + pic["pic_name"],
                    "owner": pic["owner"], "_id": pic["_id"],
                    "comment": comment, "head_pic_url": content_avatar}
            self.piclist.append(src)
        try:
            self.username = self.get_secure_cookie("user")
            doc = yield db_user.find_one({"name": self.username})
            try:
                self.liked_pic = doc["liked_pic"]
            except:
                self.liked_pic = []
            try:
                self.avatar = doc["avatar_path"] + doc["avatar_name"]
            except:
                self.avatar = "static/avatar/guest.png"
        except:
            self.username = ""
            self.liked_pic = []
        try:
            self.set_cookie("_id", str(pic["_id"]))
        finally:
            self.set_cookie("first_id", str(self.piclist[0]["_id"]))
            self.render("index.html", piclist=self.piclist,
                        liked=self.liked_pic)

route = [(r"/", MainHandler), ]
