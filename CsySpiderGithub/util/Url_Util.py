#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:chenshyiuan 
@file: Url_Util.py 
@time: 2017/04/04 
"""
import itertools
# Client ID
# cbb90c8c9e00b757a07a
# Client Secret
# 3061191bfcd5879717b3b764c574d9ec806b2aa1

# Client ID
# 593e495b0ea2dad0d3e5
# Client Secret
# 841d3b005aaf2bd71bb90c47eae4c9c58438b3eb

# Client ID
# a80fe53ff4b893920939
# Client Secret
# 7965b9914c225c1a84d8d1b78ad1044d25c5e940


client_id_list = [
    'cbb90c8c9e00b757a07a',
    '593e495b0ea2dad0d3e5',
    'a80fe53ff4b893920939'
]

client_secret_list = [
    '3061191bfcd5879717b3b764c574d9ec806b2aa1',
    '841d3b005aaf2bd71bb90c47eae4c9c58438b3eb',
    '7965b9914c225c1a84d8d1b78ad1044d25c5e940'
]

client_id_iter = itertools.cycle(client_id_list)
client_secret_iter = itertools.cycle(client_secret_list)

from distutils.log import Log

CLIENTID = 'cbb90c8c9e00b757a07a'
CLIENT_SECRET = '3061191bfcd5879717b3b764c574d9ec806b2aa1'
USER_BASE_URL = 'https://api.github.com/users'


def get_userlist_url(since=0):
    if isinstance(since, int):

        since = str(since)
        url = set_get_request_param(USER_BASE_URL, since=since, client_id=client_id_iter.next(), client_secret=client_secret_iter.next())
        return url
    elif isinstance(since, basestring):

        url = set_get_request_param(USER_BASE_URL, since=since, client_id=client_id_iter.next(), client_secret=client_secret_iter.next())
        return url
        # pass


def set_get_request_param(url, **params):  # 设置HTTP的GET方法的参数，并返回URL。
    if url is None:

        Log.error('url is none')
        return
    elif isinstance(url, basestring):  # 设置参数

        format_url = url + '?'
        for key in params:
            format_url = format_url + key + '=' + params[key] + '&'
        format_url = format_url[0:len(format_url) - 1]  # 去除掉最后的&
        return format_url


def set_client_key(url):  # 为url添加ClientKey 增加访问次数
    return set_get_request_param(url, client_id=client_id_iter.next(), client_secret=client_secret_iter.next())
    pass


# 0 29
if __name__ == '__main__':
    print get_userlist_url(0)
    print get_userlist_url(30)
    pass
