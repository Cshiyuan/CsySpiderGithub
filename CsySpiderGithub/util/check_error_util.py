#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:chenshyiuan 
@file: check_error_util.py 
@time: 2017/04/05 
"""
import logging

import time


def check_response(response):
    if response.status == 403:
        logging.error('response code is 403')
        logging.error('response body is' + response.body)
        return True
        pass
    elif response.url.split('?')[0] == 'https://api.github.com/users':
        logging.info('*************************************')
        logging.info('X-Ratelimit-Remaining is ' + response.headers['X-Ratelimit-Remaining'])
        logging.info('X-Github-Request-Id is ' + response.headers['X-Github-Request-Id'])
        logging.info('X-Ratelimit-Limit is ' + response.headers['X-Ratelimit-Limit'])
        reset_time =  int(response.headers['X-RateLimit-Reset'])
        logging.info('X-RateLimit-Reset is ' + timestamp_datetime(reset_time))
        logging.info('*************************************')
        return False

    pass

def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt


def func():
    pass


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':
    pass