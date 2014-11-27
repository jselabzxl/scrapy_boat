# -*- coding: utf-8 -*-

import re
import time
import json
from scrapy import log
from scrapy import Spider
from scrapy_boat.items import WeixinItem
from scrapy.http import Request
from BeautifulSoup import BeautifulSoup

HOST_URL = "http://weixin.sogou.com"
LIST_URL = HOST_URL + "/gzhjs?cb=sogou.weixin.gzhcb&openid={openid}&page={page}"

class SogouWeixinSearchSpider(Spider):
    """usage: scrapy crawl sogou_weixin_search --loglevel=INFO
    """
    name = "sogou_weixin_search"

    def __init__(self):
        self.openid = 'oIWsFt8kxiyiYRj6oWsCQL3hHsqU'

    def start_requests(self):
        page = 1
        search_url = self.get_search_url(self.openid, page)
        log.msg(search_url)
        request = Request(search_url)
        request.meta['page'] = page

        yield request

    def parse(self, response):
        results = []

        resp = response.body
        items = self.resp2items(resp)
        results.extend(items)

        page = response.meta['page']
        page += 1
        search_url = self.get_search_url(self.openid, page)
        log.msg(search_url)
        request = Request(search_url)
        request.meta['page'] = page
        results.append(request)

        return results

    def resp2items(self, resp):
        resp = resp.replace('\/', '/').replace('<![CDATA[', '').replace(']]>', '').replace('\u201c', '“').replace('\u201d', '”')
        soup = BeautifulSoup(resp)
        items = soup.findAll("item")
        weixins = []
        for item in items:
            key = item.find('key')
            tplid = item.find('tplid')
            classid = item.find('classid')
            docid = item.find('docid')
            title = item.find('title')
            title1 = item.find('title1')
            date = item.find('date')
            imglink = item.find('imglink')
            headimage = item.find('headimage')
            sourcename = item.find('sourcename')
            content168 = item.find('content168')
            isV = item.find('isV')
            openid = item.find('openid')
            content = item.find('content')
            showurl = item.find('showurl')
            url = item.find('url')
            pagesize = item.find('pagesize')
            lastModified = item.find('lastmodified')

            item_tuple = [key, tplid, classid, docid, title, title1, date, imglink, headimage, sourcename, content168, isV, openid, content, showurl, url, pagesize, lastModified]
            weixin = WeixinItem()
            keys = WeixinItem.RESP_ITER_KEYS
            for key in keys:
                item_value = item_tuple[keys.index(key)]
                if item_value:
                    item_value = item_value.text
                else:
                    item_value = None
                weixin[key] = item_value

            weixins.append(weixin)

        return weixins

    def get_search_url(self, openid, page):
        return LIST_URL.format(openid=openid, page=page)

