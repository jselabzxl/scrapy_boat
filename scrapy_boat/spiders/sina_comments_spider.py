# -*- coding: utf-8 -*-

import re
import time
import json
from scrapy import log
from scrapy import Spider
from scrapy.http import Request
from BeautifulSoup import BeautifulSoup

LIST_URL = "http://comment5.news.sina.com.cn/comment/skin/default.html?channel=gn&newsid={newsid}"

class SinaCommentsSpider(Spider):
    """usage: scrapy crawl sina_comments --loglevel=INFO
    """
    name = "sina_comments"

    def __init__(self):
        self.newsid = "1-1-31285984"

    def start_requests(self):
        search_url = LIST_URL.format(newsid=self.newsid)
        log.msg(search_url)
        request = Request(search_url)
        request.meta['webkit'] = True

        yield request

    def parse(self, response):
        resp = response.body
        soup = BeautifulSoup(resp)

        comments = soup.findAll("div", {"class": "comment_item"})
        log.msg(str(comments[0]))
        """
        for comment in comments:
            log.msg(str(comment))
        """

