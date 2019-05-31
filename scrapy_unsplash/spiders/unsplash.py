#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: Wade Cheung
# @Date  : 2018/6/13
# @Desc  :


import json
import sqlite3
import threading
import scrapy
from scrapy.spiders import CrawlSpider

URL0 = "https://api.unsplash.com/photos/?client_id=fa60305aa82e74134cabc7093ef54c8e2c370c47e73152f72371c828daedfcd7&page="
PATH = "E:\\wendi1\\pyplace\\scrapy_unsplash\\database\\link.db"


class UnsplashSpider(CrawlSpider):
    name = 'unsplash'
    allowed_domains = ['api.unsplash.com']

    def start_requests(self):
        createDB()  # 创建db

        start, page = 1, 100  # 要爬的页面数
        for i in range(start, page + 1):  # 从第一页开始
            url = URL0 + str(i) + '&per_page=30'
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        conn = sqlite3.connect(PATH)
        print('-------------------')

        js = json.loads(
            str(response.body_as_unicode()))  # 读取响应body
        for j in js:
            link = j["urls"]["raw"]
            sql = "INSERT INTO LINK(LINK) VALUES ('%s');" % link
            conn.execute(sql)
        semaphore = threading.Semaphore(1)  # 线程信号量，避免写入数据库时死锁
        semaphore.acquire()
        conn.commit()
        semaphore.release()


def createDB():
    """
    创建db
    :return:
    """
    conn = sqlite3.connect(
        "E:\\wendi1\\pyplace\\scrapy_unsplash\\database\\link.db")
    conn.execute("DROP TABLE IF EXISTS LINK;")  # 重新运行删掉数据库
    conn.execute(
        "CREATE TABLE LINK (ID INTEGER PRIMARY KEY AUTOINCREMENT,LINK VARCHAR(255));")
