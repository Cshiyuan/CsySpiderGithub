#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:chenshyiuan 
@file: check_error_util.py 
@time: 2017/04/05 
"""
import logging

def check_error(response):
    if response.status == 403:
        logging.error('response code is 403')
        logging.error('response body is' + response.body)
        return True
        pass
    pass

def func():
    pass


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':
    pass