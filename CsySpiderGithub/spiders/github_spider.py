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
from CsySpiderGithub.util.check_error_util import check_response


class StackSpider(scrapy.Spider):
    name = "github_spider"
    allowed_domains = [
        "github.com",
        "api.github.com"
    ]

    handle_httpstatus_list = [403]

    download_delay = 0.25

    headers = {
        'User-Agent': "Github_API_REQUESTS"
    }

    def start_requests(self):
        self._request_count = 0
        self._user_since = 0
        start_url = get_userlist_url(0)
        yield scrapy.Request(url=start_url, callback=self.parse)
        pass

    def parse(self, response):
        # 判断错误
        if check_response(response):
            return
        # 遍历users获取每个user的repos
        json_response = json.loads(response.body)

        yield scrapy.Request(
            'https://api.github.com/users/pergesu/repos?client_secret=3061191bfcd5879717b3b764c574d9ec806b2aa1&client_id=cbb90c8c9e00b757a07a',
            self.parse_user_repos)

        for i, user in enumerate(json_response):

            # 遍历用户信息
            url_user = user['url']
            url_user = set_client_key(url_user)
            if url_user:
                logging.info('try to crawl ' + user['login'] + ' info' + ' repos info with request id ' + str(
                    self._request_count))
                self._request_count += 1
                yield scrapy.Request(url_user, self.parse_user_info)

            # 遍历用户repos信息
            url_repos = user['repos_url']
            url_repos = set_client_key(url_repos)
            if url_repos:
                logging.info(
                    'try to crawl ' + user['login'] + ' repos info with request id ' + str(self._request_count))
                self._request_count += 1
                yield scrapy.Request(url_repos, self.parse_user_repos)

            # 如果已经遍历到了尽头，则开始下一轮遍历。
            if i == len(json_response) - 1:
                self._user_since = user['id']  # 记录下一步的since
                next_users_url = get_userlist_url(self._user_since)
                logging.warning('start next users_url \n' + next_users_url)
                yield scrapy.Request(next_users_url, self.parse)
                pass

    def parse_user_repos(self, response):
        # 判断错误
        if check_response(response):
            return

        repos_json_response = json.loads(response.body)

        #如果库为空
        if len(repos_json_response) == 0:
            own_name = response.url.split('?')[0].split('/')[-2]
            logging.warning(own_name + '\'s repos is empty!')
            pass
        else:
            owner = repos_json_response[0]['owner']['login']
            for repos in repos_json_response:
                repos_item = Github_Repos_Item()
                repos_item['id'] = repos['id']
                repos_item['owner_id'] = repos['owner']['id']
                repos_item['name'] = repos['name']
                repos_item['full_name'] = repos['full_name']
                repos_item['language'] = repos['language']
                repos_item['size'] = repos['size']
                repos_item['created_at'] = repos['created_at']
                repos_item['updated_at'] = repos['updated_at']
                repos_item['pushed_at'] = repos['pushed_at']
                repos_item['forks'] = repos['forks']
                repos_item['watchers'] = repos['watchers']
                repos_item['stargazers_count'] = repos['stargazers_count']
                yield repos_item
            logging.info('success to crawl ' + owner + '\'s repos info!')

    def parse_user_info(self, response):
        # 判断错误
        if check_response(response):
            return

        user = json.loads(response.body)
        user_item = Github_User_Item()
        user_item['id'] = user['id']
        user_item['username'] = user['login']
        user_item['repos_url'] = user['repos_url']
        user_item['homepage_url'] = user['html_url']
        user_item['created_at'] = user['created_at']
        user_item['updated_at'] = user['updated_at']
        user_item['following'] = user['following']
        user_item['followers'] = user['followers']
        user_item['public_gists'] = user['public_gists']
        user_item['public_repos'] = user['public_repos']
        user_item['location'] = user['location']
        yield user_item

        logging.info('success to crawl ' + user['login'] + '\'s info!')

    pass

    def close(spider, reason):
        logging.warning('close with reason :')
        logging.warning(reason)
        logging.warning('since is ' + str(spider._user_since))
        pass
