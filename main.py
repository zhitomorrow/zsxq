#!/usr/bin/python3  
# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 22:55
# @Author  : lzm
# @File    : main.py

import spider.digests_topic as topic


def main():
    spider = topic.digests_spider()
    spider.gather_data('questions', 10000)
    # spider.gather_data('digests', 10)


if __name__ == '__main__':
    main()
