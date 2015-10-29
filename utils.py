'''
Created on Oct 29, 2015

@author: ev0l
'''
import os


def mkdir(path):
    '''
    新建目录函数,先检查存在性,通过接受传入的参数新建
    此处新建名为当天日期
    '''
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
