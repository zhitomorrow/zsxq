#!/usr/bin/python3  
# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 22:43
# @Author  : lzm
# @File    : mongo_connection.py

import pymongo


class mongo_connection(object):

    def get_collection(self):
        """
        获取到集合
        :return:
        """
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client['zsxq']
        return db['articles']

    def insert(self, data: 'list'):
        """
        插入数据
        :param data: list类型
        :return:
        """
        print('需要插入的数据条数>>>%s' % (len(data)))
        result = self.get_collection().insert_many(data)


# single = mongo_connection()
# conn = single.get_collection()
# data = [
#     {'articleId': '2', 'content': 'test2', 'createTime': '2020-04-28T12:20:16.419+0800'},
#     {'articleId': '2', 'content': 'test2', 'createTime': '2020-04-28T12:20:16.419+0800'},
#     {'articleId': '2', 'content': 'test2', 'createTime': '2020-04-28T12:20:16.419+0800'},
#     {'articleId': '2', 'content': 'test2', 'createTime': '2020-04-28T12:20:16.419+0800'}
# ]
# single.insert(conn, data)
