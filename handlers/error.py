'''
Created on Oct 29, 2015

@author: ev0l
'''
from handlers import BaseHandler


class ErrorHandler(BaseHandler):
    def get(self):
        self.write_error(404)

    def write_error(self, status_code):
        if status_code == 404:
            self.render("404.html")
        elif status_code == 500:
            self.write("500 error")
        else:
            self.write('error:' + str(status_code))
            
