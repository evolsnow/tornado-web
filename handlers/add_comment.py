'''
Created on Oct 29, 2015

@author: ev0l
'''
import time
import tornado.gen
from tornado.ioloop import IOLoop

from bson import ObjectId
from handlers import BaseHandler


class AddCommentHandler(BaseHandler):
    '''
    评论添加
    '''
    @tornado.gen.coroutine
    def post(self):
        user = str(self.get_secure_cookie("user"))
        pic_id = ObjectId(self.get_argument("id")[1:])
        comment = self.get_argument("comment")
        db_pic = self.application.db.pic
        if comment:
            new_comment = {user: comment}
            dic = {"comment": new_comment}
            try:
                yield db_pic.update({'_id': pic_id}, {'$push': dic})
            except:
                yield db_pic.update({'_id': pic_id}, {'$set': dic})
            # TODO:延迟动画应交给前端js完成
            yield tornado.gen.Task(IOLoop.instance().add_timeout, time.time() + 0.5)
            result = '<a class="v_a" href="/user/' + user + '">' + \
                    user + '</a>: <span>' + comment + '</span><br />'
            self.write(result)

route = [(r"/addcomment", AddCommentHandler), ]
