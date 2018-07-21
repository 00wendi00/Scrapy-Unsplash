# -*- coding: utf-8 -*-
import json
import sqlite3
import threading
import scrapy
from scrapy.spiders import CrawlSpider


class UnsplashSpider(CrawlSpider):
    name = 'unsplash'
    allowed_domains = ['api.unsplash.com']

    def start_requests(self):
        createDB()  # 创建数据库

        start, page = 1, 1,  # 要爬的页面数
        for i in range(start, page + 1):  # 从第一页开始
            url = 'https://api.unsplash.com/photos/?client_id=fa60305aa82e74134cabc7093ef54c8e2c370c47e73152f72371c828daedfcd7&page=' + str(
                i) + '&per_page=30'
            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        conn = sqlite3.connect("E:\\wendi1\\pyplace\\scrapy_unsplash\\database\\link.db")  # 连接数据库
        print('-------------------')

        js = json.loads(str(response.body_as_unicode()))  # 读取响应body，并转化成可读取的json
        for j in js:
            link = j["urls"]["raw"]
            sql = "INSERT INTO LINK(LINK) VALUES ('%s');" % link  # 将link插入数据库
            conn.execute(sql)
        semaphore = threading.Semaphore(1)  # 引入线程信号量，避免写入数据库时死锁
        semaphore.acquire()  # P操作
        conn.commit()  # 写入数据库，此时数据库文件独占
        semaphore.release()  # V操作


def createDB():  # 创建数据库
    conn = sqlite3.connect("E:\\wendi1\\pyplace\\scrapy_unsplash\\database\\link.db")  # Sqlite是一个轻量数据库，不占端口，够用
    conn.execute("DROP TABLE IF EXISTS LINK;")  # 重新运行删掉数据库
    conn.execute("CREATE TABLE LINK ("  # 创建属性ID：主键自增；属性LINK：存放图片链接
                 "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "LINK VARCHAR(255));")
