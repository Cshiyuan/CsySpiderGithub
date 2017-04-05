#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:chenshyiuan 
@file: check_error_util.py 
@time: 2017/04/05 
"""
import logging

def check_response(response):
    if response.status == 403:
        logging.error('response code is 403')
        logging.error('response body is' + response.body)
        return True
        pass
    else:
        logging.info('X-Ratelimit-Remaining is ' + response.headers['X-Ratelimit-Remaining'])
        logging.info('X-Github-Request-Id is ' + response.headers['X-Github-Request-Id'])
        logging.info('X-Ratelimit-Limit is ' + response.headers['X-Ratelimit-Limit'])
        return False

    pass

def func():
    pass


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':
    pass