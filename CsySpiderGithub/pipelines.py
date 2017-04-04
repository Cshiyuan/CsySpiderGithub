# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

SERVER_ID = "119.29.186.160"
SERVER_PORT = 27017
SERVER_DB = "github_info"
USER_Table = "USER_TABLE"


class GithubPipeline(object):
    # spider运行开始时候执行
    def open_spider(self, spider):
        self.mongo_client = pymongo.MongoClient(SERVER_ID, SERVER_PORT)  # 获得连接
        self.mongo_github_db = self.mongo_client[SERVER_DB]  # 获得数据库
        self.user_table = self.mongo_github_db[USER_Table]  # 创建表明
        pass

    # 将相关的item添加到数据库表中
    def process_item(self, item, spider):

        self.user_table.insert(dict(item))

        return item
        pass

    # spider运行结束时候执行
    def close_spider(self, spider):
        pass
