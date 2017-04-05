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
from CsySpiderGithub.items import Github_Repos_Item
from CsySpiderGithub.items import Github_User_Item
from  CsySpiderGithub.util.Url_Util import set_get_request_param
from  CsySpiderGithub.util.Url_Util import set_client_key


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

            # 遍历用户信息
            url_user = user['url']
            url_user = set_client_key(url_user)
            if url_user:
                yield scrapy.Request(url_user, self.parse_user_info)

            # 遍历用户repos信息
            logging.info('start to spider' + user['username'] + 'is repos')
            url_repos = user['repos_url']
            url_repos = set_client_key(url_repos)
            if url_repos:
                yield scrapy.Request(url_repos, self.parse_user_repos)

            # 如果已经遍历到了尽头，则开始下一轮遍历。
            if i == len(jsonresponse) - 1:
                next_users_url = get_userlist_url(user['id'])
                logging.info('start next users_url' + next_users_url)
                yield scrapy.Request(next_users_url, self.parse)
                pass

    def parse_user_repos(self, response):

        repos_json_response = json.loads(response.body)
        for repos in repos_json_response:
            repos_item = Github_Repos_Item()
            repos_item['full_name'] = repos['full_name']
            repos_item['language'] = repos['language']

            yield repos_item

    def parse_user_info(self, response):

        json_response = json.loads(response.body)
        user_item = Github_User_Item()

        user_item['id'] = json_response['id']
        user_item['username'] = json_response['login']
        user_item['repos_url'] = json_response['repos_url']
        user_item['homepage_url'] = json_response['html_url']
        user_item['created_at'] = json_response['created_at']
        user_item['updated_at'] = json_response['updated_at']
        user_item['following'] = json_response['following']
        user_item['followers'] = json_response['followers']
        user_item['public_gists'] = json_response['public_gists']
        user_item['public_repos'] = json_response['public_repos']
        user_item['location'] = json_response['location']
        yield user_item

        pass
