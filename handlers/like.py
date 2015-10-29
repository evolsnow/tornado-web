'''
Created on Oct 29, 2015

@author: ev0l
'''
import tornado.gen

from bson import ObjectId
from handlers import BaseHandler


class LikeOrNotHandler(BaseHandler):
    '''
    点赞
    '''
    @tornado.gen.coroutine
    def post(self):
        user = str(self.get_secure_cookie("user"))
        pic_id = ObjectId(self.get_argument("id")[5:])
        status = self.get_argument("status")
        db_user = self.application.db.user
        dic = {"liked_pic": pic_id}
        if status == "yes":
            yield db_user.update({"name": user}, {'$push': dic})
        if status == "no":
            yield db_user.update({'name': user}, {'$pop': dic})

route = [(r"/like", LikeOrNotHandler), ]
