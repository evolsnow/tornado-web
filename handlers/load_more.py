'''
Created on Oct 29, 2015

@author: ev0l
'''
import time
import tornado.gen
from tornado.ioloop import IOLoop

from bson import ObjectId
from handlers import BaseHandler


class LoadMoreHandler(BaseHandler):
    '''
    图片加载函数,一次加载options.loadnum张,
    如果最后加载张数不达,则全部加载
    '''
    @tornado.gen.coroutine
    def get(self):
        # TODO:动画效果应该由前端js完成，而非线程休眠
        yield tornado.gen.Task(IOLoop.instance().add_timeout, time.time() + 0.8)
        db_pic = self.application.db.pic
        db_user = self.application.db.user
        cid = ObjectId(self.get_cookie("_id"))
        cursor = db_pic.find({'_id': {'$lt': cid}}).sort([('_id', -1)])
        try:
            cursor = cursor[0: self.application.loadnum]
        except:
            cursor = cursor
        doc = yield db_user.find_one({"name": self.get_secure_cookie("user")})
        try:
            liked_pic = doc["liked_pic"]
        except:
            liked_pic = []
        while (yield cursor.fetch_next):
            pic = cursor.next_object()
            owner_avatar = yield db_user.find_one({"name": pic["owner"]})
            try:
                content_avatar = owner_avatar["avatar_path"] + \
                        owner_avatar["avatar_name"]
            except:
                content_avatar = "static/avatar/guest.png"
            pic["picurl"] = pic["pic_path"] + pic["pic_name"]
            pic["head_pic_url"] = content_avatar
            self.set_cookie("_id", str(pic["_id"]))
            try:
                pic["comment"] = pic["comment"]
            except:
                pic["comment"] = None
            string = self.render_string("modules/picture.html",
                                        picture=pic, liked=liked_pic)
            self.write(string)

route = [(r"/loadmore", LoadMoreHandler), ]
