import re

import requests
from bs4 import BeautifulSoup
from lxml import etree
news_url="https://news.yahoo.co.jp/articles/54e6be2a11395f4bb689e54fe43e9784f8ebbf3e?source=rss"
u2="https://news.yahoo.co.jp/articles/2981fcc9f7f14f0af64c5644d8c02b79f2bab4a6"
from bs4 import BeautifulSoup

def fetch_news_content(news_url):
    try:
        # 发送 HTTP 请求获取新闻页面的 HTML 内容
        # 设置伪装标头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'B=ba41jh5ii25ba&b=3&s=9g; A=8f7mi1pii25ba&sd=A&t=1696666986&u=1696666986&v=1; XA=8f7mi1pii25ba&sd=A&t=1696666986&u=1696666986&v=1; XB=ba41jh5ii25ba&b=3&s=9g'
        }
        response = requests.get(news_url,headers=headers)
        # 检查响应状态码
        if response.status_code == 200:
            # 使用 BeautifulSoup 解析 HTML 内容
            soup = BeautifulSoup(response.text, 'html.parser')
           # 将Beautiful Soup的文档对象转换为lxml的Element对象
            element = etree.HTML(str(soup))
            # 使用XPath选择具有特定数据属性和类名的<p>元素
            news_content_elements = element.xpath(
                '//p[@class="sc-iMCRTP ePfheF yjSlinkDirectlink highLightSearchTarget"]/text()')
            # print(news_content_elements)
            if news_content_elements:
                # 提取每个段落的文本内容并连接起来
                news_content = ''.join(news_content_elements)
                # print(news_content)
                return news_content
            else:
                print("未找到匹配的新闻内容元素。")
        else:
            return "请求失败，请检查 URL 或网络连接。"
    except Exception as e:
        return f"发生错误：{str(e)}"
def getContent(start_url):
    page=1
    content=''
    while page:
        current_url = f"{start_url}?page={page}"
        print(current_url)
        res=requests.get(current_url)
        if res.status_code == 200:
            content+=fetch_news_content(current_url)
            return content
        else:
            break
        page+=1

fetch_news_content(u2)