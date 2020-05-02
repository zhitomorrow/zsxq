# -*- coding: utf-8 -*-

"""
@Time        : 2020/4/29
@Author      : LZM
@File        : digests_topic
@Description : 采集主题
"""

import requests
import urllib.parse as ul
import json
import jsonpath
import re
import time
import data.mongo_connection as connection


class digests_spider(object):

    # topic_type: topic类型：with_files 文件主题；questions 问答主题；by_owner 只看星主；digests 精华主题
    def request_page(self, topic_type, end_time):
        url = 'https://api.zsxq.com/v1.10/groups/222454121411/topics?scope=%s&count=20' % topic_type
        print(end_time)
        if end_time.strip != '':
            end_time = ul.quote(end_time, encoding='utf-8')
            url = url + "&end_time=" + end_time

        print('请求的url>>>%s' % url)

        headers = {
            'Cookie': 'xxxxxxxx',  # TODO 需要换成自己 的COOKIE
            'Host': 'api.zsxq.com',
            'Origin': 'https://wx.zsxq.com',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'h-CN,zh;q=0.9',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
            'User-Agent': ''  # TODO 换成自己的UA
        }

        response = requests.get(url, headers=headers)
        print(response.text)
        return response.text

    def parse_data_digests(self, data):
        articles = []
        next_page_params = ''
        json_data = json.loads(data)
        success = jsonpath.jsonpath(json_data, '$.succeeded')
        if success[0]:
            topics = json_data['resp_data']['topics']
            for i in range(0, len(topics)):
                # print('id>>%s' % ids[i])
                topic = topics[i]
                data_time = topic['create_time']
                content = topic['talk']['text']
                # content = re.sub(r'<[^>]*>', '', content).strip()
                content = content.replace('\n', '<br>')
                # 处理图片
                images = []
                if topic.get('talk').get('images'):
                    for img in topic.get('talk').get('images'):
                        url = img.get('large').get('url')
                        images.append(url)
                row = {
                    'articleId': topic['topic_id'],
                    'createTime': data_time,
                    'content': content,
                    'images': ','.join(images),
                    'type': 'digests'
                }
                articles.append(row)
                print('--------------------------------%s-----------------------------------------------' % str(i))
                if i == len(topics) - 1:
                    next_page_params = data_time
        if next_page_params != '':
            conn = connection.mongo_connection()
            conn.insert(data=articles)
            print('next>>>%s' % next_page_params)
            # 处理下一页的请求参数
            if next_page_params[20:23] == "000":
                next_page_params = next_page_params[:20] + "999" + next_page_params[23:]
            else:
                res = int(next_page_params[20:23]) - 1
                # zfill 函数补足结果前面的零，始终为3位数
                next_page_params = next_page_params[:20] + str(res).zfill(3) + next_page_params[23:]
            print(next_page_params)
        return next_page_params

    def parse_data_question(self, data):
        """
        解析question类型的数据
        :param data:
        :return:
        """
        articles = []
        next_page_params = ''
        json_data = json.loads(data)
        success = jsonpath.jsonpath(json_data, '$.succeeded')
        if success[0]:
            topics = json_data['resp_data']['topics']
            for i in range(0, len(topics)):
                topic = topics[i]
                data_time = topic['create_time']
                question_text = topic['question']['text']
                answer_text = topic['answer']['text']  # 处理图片
                question_images = []
                if topic.get('question').get('images'):
                    for img in topic.get('question').get('images'):
                        url = img.get('large').get('url')
                        question_images.append(url)
                answer_images = []
                if topic.get('answer').get('images'):
                    for img in topic.get('answer').get('images'):
                        url = img.get('large').get('url')
                        question_images.append(url)
                row = {
                    'articleId': topic['topic_id'],
                    'createTime': data_time,
                    'question': question_text,
                    'answer': answer_text,
                    'images': ','.join(question_images),
                    'answerImages': ','.join(answer_images),
                    'type': 'question'
                }
                articles.append(row)
                print('--------------------------------%s-----------------------------------------------' % str(i))
                if i == len(topics) - 1:
                    next_page_params = data_time
        if next_page_params != '':
            conn = connection.mongo_connection()
            conn.insert(data=articles)
            print('next>>>%s' % next_page_params)
            # 处理下一页的请求参数
            if next_page_params[20:23] == "000":
                next_page_params = next_page_params[:20] + "999" + next_page_params[23:]
            else:
                res = int(next_page_params[20:23]) - 1
                # zfill 函数补足结果前面的零，始终为3位数
                next_page_params = next_page_params[:20] + str(res).zfill(3) + next_page_params[23:]
            print(next_page_params)
        return next_page_params

    def gather_data(self, post_type: 'str', limit: 'int'):
        next_params = ''
        for page in range(0, limit):
            print('第%s页的请求参数:[%s]' % (page, next_params))
            text = self.request_page(post_type, next_params)
            if post_type == 'digests':
                next_params = self.parse_data_digests(text)
            elif post_type == 'questions':
                next_params = self.parse_data_question(text)
            if next_params == '':
                break
            time.sleep(30)  # 每页访问间隔10s，科学访问
