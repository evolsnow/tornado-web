'''
Created on Oct 29, 2015

@author: ev0l
'''
import tornado.web


class PictureModule(tornado.web.UIModule):
    '''
    ui渲染模块,渲染首页用
    '''
    def render(self, picture, liked):
        return self.render_string("modules/picture.html", picture=picture,
                                  liked=liked)
