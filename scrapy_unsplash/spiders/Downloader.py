# -*- encoding:utf-8 -*-
import sqlite3, urllib.request, threadpool  # sqlite3：管理数据库；urllib：下载文件；threadpool：线程池


class Downloader:
    def __init__(self, urls, folder, threads=10):  # 初始化函数
        self.urls = urls  # 需要下载的网址list
        self.folder = folder  # 保存的文件目录
        self.threads = threads  # 并发线程数

    def run(self):
        pool = threadpool.ThreadPool(self.threads)  # 新建线程池
        requests = threadpool.makeRequests(self.downloader, self.urls)  # 新建请求
        [pool.putRequest(i) for i in requests]  # 将请求装入线程池
        pool.wait()  # 等待运行完成

    def downloader(self, url):
        pre = url.split('/')[-1]
        # name = pre if pre.split(".")[-1] in ["jpg", "png", "bmp"] else pre + ".jpg"  # 文件名
        name = pre[:19] + ".jpg"  # 文件名
        print(self.folder + "/" + name)
        self.auto_down(url, self.folder + "/" + name)  # 下载

    def auto_down(self, url, filename):  # 处理出现网络不好的问题，重新下载
        try:
            urllib.request.urlretrieve(url, filename)
        except urllib.request.URLError as e:
            print(str(e) + 'Network Error,redoing download :' + url)
            self.auto_down(url, filename)  # 递归


if __name__ == "__main__":
    urls = []
    conn = sqlite3.connect("e:/wendi1/pyplace/scrapy_unsplash/database/link.db")  # 连接数据库
    cursor = conn.execute("SELECT LINK FROM LINK WHERE ID <= 30")  # 选择总数
    for row in cursor:
        urls.append(row[0])
    pd = Downloader(urls, "e:/wendi1/pyplace/scrapy_unsplash/files", threads=50)  # 新建下载器
    pd.run()
