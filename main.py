import codecs
import copy
import csv
import json
import math
import os
import random
import sys
import traceback
import webbrowser
from collections import OrderedDict
from datetime import date, datetime, timedelta
from time import sleep
import requests
from lxml import etree
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
import requests
import feedparser
from html import unescape
import time
import re
import json
from fetch_news_content import getContent
from news import News
from Baidu_Text_transAPI import translate
import threading
import sched
import time

n=10
class data_spider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
        }
        self.news_list = []  # 用于存储采集到的数据
    def Spider(self,url):
        res=requests.get(url)
        if res.status_code == 200:
            #使用feedparser解析RSS数据
            rss_data = feedparser.parse(res.text)
            # 输出RSS的标题和链接
            # print(f"RSS标题: {rss_data.feed.title}")
            # print(f"RSS链接: {rss_data.feed.link}")
            # 遍历RSS项目并提取信息
            for index, item in enumerate(rss_data.entries):
                if index < 10:  # 只遍历前10个条目
                    news = News(item.title, item.link, item.description, item.published)
                    self.news_list.append(news)
                else:
                    break  # 如果已经添加了10个条目，退出循环
        else:
            print("请求失败，请检查URL或网络连接。")

    # 显示新闻列表
    def show_news_list(self):
        print("最新的十条新闻：")
        for i in range (1,n+1):
            print(f"{i}. {self.news_list[i-1].title}")

    def selctNews(self,num):
        if 0 <= num <=len(self.news_list):
            return self.news_list[num-1].link.replace("?source=rss","")
        else:
            return None

def helpPrint():
    print("---------------------")
    print("1.按t翻译")
    print("2.按r返回新闻列表")


def clear_console():
    os.system('cls')  # 使用 'cls' 命令清除控制台内容

# 定义更新新闻列表的函数
def update_newslist():
    global my_list
    while True:
        # 在这里执行更新列表的操作，可以是从外部数据源获取新数据
        timestamp = time.time()
        # print("start.....")
        data_spider.Spider('https://news.yahoo.co.jp/rss/categories/life.xml')
        time.sleep(600)  # 每隔10分钟（600秒）更新一次列表


if __name__ == "__main__":
    data_spider = data_spider()
    # 创建后台线程
    update_thread = threading.Thread(target=update_newslist, daemon=True)
    # 启动后台线程
    update_thread.start()
    data_spider.Spider('https://news.yahoo.co.jp/rss/categories/life.xml')
    while True:
        data_spider.show_news_list()
        choice = input("请选择新闻（1-10），或按 q 退出：")
        if choice == 'q':
            clear_console()
            break
        while int(choice)>=1 and int(choice)<=10:
            # print(data_spider.selctNews(int(choice)))
            print(getContent(data_spider.selctNews(int(choice))))
            helpPrint()
            choice2=input()
            if choice2 == 'r':
                clear_console()
                break
            if choice2 == 't':
                translate(getContent(data_spider.selctNews(int(choice))))
                print('\n')
                clear_console()
                break

        # data_spider.Spider('https://news.yahoo.co.jp/rss/categories/life.xml')  # 调用Spider方法来执行爬取任务
        # time.sleep(600)  # 暂停10分钟（600秒）

