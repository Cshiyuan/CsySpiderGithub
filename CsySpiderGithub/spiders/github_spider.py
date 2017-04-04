#!usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author:chenshyiuan 
@file: github_spider.py 
@time: 2017/04/04 
"""
import scrapy
import json
import logging
from CsySpiderGithub.util.Url_Util import get_userlist_url
from CsySpiderGithub.items import CsyspiderforgithubItem
from  CsySpiderGithub.util.Url_Util import set_get_request_param
from  CsySpiderGithub.util.Url_Util import set_client_key

from CsySpiderGithub.github_repos_item import ReposItem


class StackSpider(scrapy.Spider):
    name = "github_spider"
    allowed_domains = [
        "github.com",
        "api.github.com"
    ]

    download_delay = 1

    headers = {
        'User-Agent': "Github_API_REQUESTS"
    }

    start_urls = [
        "https://api.github.com/users?since=0&client_id=cbb90c8c9e00b757a07a&client_secret=3061191bfcd5879717b3b764c574d9ec806b2aa1",
    ]

    def parse(self, response):
        # 遍历users获取每个user的repos
        jsonresponse = json.loads(response.body)

        for i, user in enumerate(jsonresponse):

            item = CsyspiderforgithubItem()
            item['username'] = user['login']
            item['repos_url'] = user['repos_url']
            item['id'] = user['id']
            yield item
            url_repos = user['repos_url']
            if url_repos:
                url_repos = set_client_key(url_repos)
                logging.info('start to spider' + item['username'] + 'is repos')

                yield scrapy.Request(url_repos, self.parse_user_repos)

            # 如果已经遍历到了尽头，则开始下一轮遍历。
            if i == len(jsonresponse) - 1:
                next_users_url = get_userlist_url(item['id'])
                logging.info('start next users_url' + next_users_url)
                yield scrapy.Request(next_users_url, self.parse)
                pass

    def parse_user_repos(self, response):

        repos_json_response = json.loads(response.body)
        for repos in repos_json_response:
            repos_item = ReposItem()
            repos_item['full_name'] = repos['full_name']
            repos_item['language'] = repos['language']

            yield repos_item
