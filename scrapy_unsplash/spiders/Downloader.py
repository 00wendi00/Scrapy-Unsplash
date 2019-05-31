#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: Wade Cheung
# @Date  : 2018/6/13
# @Desc  :


import sqlite3
import threadpool

from urllib import request


class Downloader:
    def __init__(self, urls, folder, threads=10):  # 初始化函数
        """
        :param urls: 需要下载的网址list
        :param folder: 保存的文件目录
        :param threads: 并发线程数
        """
        self.urls = urls
        self.folder = folder
        self.threads = threads

    def run(self):
        pool = threadpool.ThreadPool(self.threads)
        requests = threadpool.makeRequests(self.downloader, self.urls)
        # 将请求装入线程池, 等待运行完成
        [pool.putRequest(i) for i in requests]
        pool.wait()

    def downloader(self, url):
        pre = url.split('/')[-1]
        # name = pre if pre.split(".")[-1] in ["jpg", "png", "bmp"] else pre + ".jpg"
        name = pre[:19] + ".jpg"  # 文件名
        print(self.folder + "/" + name)
        self.auto_down(url, self.folder + "/" + name)

    def auto_down(self, url, filename):  # 处理出现网络不好的问题，重新下载
        try:
            request.urlretrieve(url, filename)
        except request.URLError as e:
            print(str(e) + 'Network Error,redoing download :' + url)
            self.auto_down(url, filename)


if __name__ == "__main__":
    urls = []
    conn = sqlite3.connect(
        "e:/wendi1/pyplace/scrapy_unsplash/database/link.db")
    cursor = conn.execute("SELECT LINK FROM LINK WHERE ID <= 30")  # 选择总数
    for row in cursor:
        urls.append(row[0])
    download = Downloader(urls, "e:/wendi1/pyplace/scrapy_unsplash/files",
                          threads=50)
    download.run()
