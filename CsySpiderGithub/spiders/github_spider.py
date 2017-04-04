#!usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author:chenshyiuan 
@file: github_spider.py 
@time: 2017/04/04 
"""
import scrapy
import json
import logging
from CsySpiderGithub.items import CsyspiderforgithubItem
from CsySpiderGithub.github_repos_item import ReposItem


# Client ID
# cbb90c8c9e00b757a07a
# Client Secret
# 3061191bfcd5879717b3b764c574d9ec806b2aa1

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

        for user in jsonresponse:
            # print user['login']
            #
            item = CsyspiderforgithubItem()
            item['username'] = user['login']
            item['repos_url'] = user['repos_url']
            yield item
            url_repos = user['repos_url']
            if url_repos:
                # print(url_repos)
                url_repos = url_repos + \
                            "?client_id=cbb90c8c9e00b757a07a&client_secret=3061191bfcd5879717b3b764c574d9ec806b2aa1"
                logging.info(url_repos)
                yield scrapy.Request(url_repos, self.parse_user_repos)

        n = 90
        while n < 1000:
            url = "https://api.github.com/users?since=" + '%d' % n + \
                  "?client_id=cbb90c8c9e00b757a07a&client_secret=3061191bfcd5879717b3b764c574d9ec806b2aa1"
            logging.info(url)
            n = n + 30
            yield scrapy.Request(url, self.parse)
        yield jsonresponse

    def parse_user_repos(self, response):

        # print response.body

        repos_json_response = json.loads(response.body)
        for repos in repos_json_response:
            repos_item = ReposItem()
            repos_item['full_name'] = repos['full_name']
            repos_item['language'] = repos['language']

            logging.info('try to save to mongodb with %s and language is %s' % (repos['full_name'], repos['language']))

            yield repos_item
