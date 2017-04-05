# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Github_User_Item(Item):
    # define the fields for your item here like:
    id = Field()
    username = Field()
    repos_url = Field()
    html_url = Field()
    homepage_url = Field()
    created_at = Field()
    updated_at = Field()
    following = Field()
    followers = Field()
    public_gists = Field()
    public_repos = Field()
    location = Field()


class Github_Repos_Item(Item):
    # define the fields for your item here like:
    id = Field()  # 唯一id
    name = Field()  # 名称
    full_name = Field()  # 全名
    language = Field()  # language 的语言类型
    size = Field()
    create_at = Field()
    updated_at = Field()
    pushed_at = Field()
    forks = Field()
    watchers = Field()
    stargazers_count = Field()  # start数量

    pass
