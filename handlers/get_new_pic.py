'''
Created on Oct 29, 2015

@author: ev0l
'''
import tornado.gen

from bson import ObjectId
from handlers import BaseHandler


class GetNewPicHandler(BaseHandler):
    '''
    获取新上传的图片
    '''
    @tornado.gen.coroutine
    def get(self):
        db_pic = self.application.db.pic
        first_id = ObjectId(self.get_cookie("first_id"))
        cursor = db_pic.find({'_id': {'$gt': first_id}}).sort([('_id', -1)])
        idlist = []
        while (yield cursor.fetch_next):
            pic = cursor.next_object()
            pic["picurl"] = pic["pic_path"] + pic["pic_name"]
            idlist.append(pic["_id"])
            try:
                pic["comment"] = pic["comment"]
            except:
                pic["comment"] = None
            string = self.render_string("modules/picture.html",
                                        picture=pic, liked=[])
            self.write(string)
        try:
            self.set_cookie("first_id", str(idlist[0]))
        finally:
            return

route = [(r"/getnewpic", GetNewPicHandler), ]
