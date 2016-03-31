#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import Queue
import HTMLParser
from bs4 import BeautifulSoup
from weibo_crawler import WeiboCrawler


class mycrawler(WeiboCrawler):

    domain = 'http://weibo.cn'
    start_url = 'http://weibo.cn'

    host = "weibo.cn"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36"
    cookie = "T_WM=bd230a5604cdb56bbe4314af5958fee3; SUB=_2A257_nv8DeRxGeNO7VUU8yzFzziIHXVZAQW0rDV6PUJbstBeLUfBkW1LHestAc5CP2aVdWeNBDhuCgt5SNU4Tg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFGTX4oOj01Hw_XFxKFbxQr5JpX5o2p; SUHB=0sqxHehL6B7UvD; SSOLoginState=1459227564; gsid_CTandWM=4uYDCpOz53uLLl4dRLMZ4lgiofe"
    # referer = 'http://weibo.cn'
    referer = "http://login.sina.com.cn/sso/login.php?url=http%3A%2F%2Fweibo.cn%2F&_rand=1459153356.0121&gateway=1&service=sinawap&entry=sinawap&useticket=1&returntype=META&sudaref=&_client_version=0.6.16",

    def start(self):
        crawl_queue = Queue.Queue()
        crawled_queue = list()
        crawl_queue.put(self.start_url)
        while True:
            url = crawl_queue.get()
            response = self.get_response_from_url(url)
            if self.if_parse(url):
                self.parse(response)
                crawled_queue.append(url)
            urls = self.get_links_from_html(response.text)
            for new_url in urls:
                if self.if_parse(new_url) or self.if_follow(new_url) \
                    and new_url not in crawled_queue:
                    crawl_queue.put(new_url)

    def if_parse(self, url):
        user_home = re.compile('/u/\d+$')
        if user_home.search(url):
            return True
        return False

    def if_follow(self, url):
        fans = re.compile('/fans$')
        follow = re.compile('/follow$')
        if fans.search(url) or follow.search(url):
            return True
        return False

    def parse(self, response):
        html_parser = HTMLParser.HTMLParser()
        print 'response.url: %s' % response.url
        with open('weibo.text', 'w+') as f:
            f.write(response.text.encode('utf8'))
        page = BeautifulSoup(response.text, 'lxml')
        message = page.body.span.text
        print message
        ti = html_parser.unescape(message)
        print ti
        title = ti.split(' ')
        for t in title:
            print t
        contents = self.get_contents(response.url)

    def get_contents(self, url):
        """下载用户原创微博页面"""
        contents = []
        for i in range(1, 6):
            content_url = url + '?filter=1&page=%s' % i
            response = self.get_response_from_url(content_url)
            content = self.parse_page(response)
            contents.extend(content)
        return contents

    def parse_page(self, response):
        """解析页面中的微博正文"""
        page = BeautifulSoup(response.text, 'lxml')
        divs = page.find_all('div')
        content = []
        for div in divs:
            if u'class' and u'id' in div.attrs.keys() and u'c' in div.attrs[u'class']:
                text = div.span.text
                print text
                content.append(text)
        return content


m = mycrawler()
