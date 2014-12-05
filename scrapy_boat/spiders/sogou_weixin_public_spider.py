# -*- coding: utf-8 -*-

import re
import time
import json
from scrapy import log
from scrapy import Spider
from scrapy.http import Request
from scrapy_boat.items import ScrapyBoatItem
from BeautifulSoup import BeautifulSoup

HOST_URL = "http://weixin.sogou.com"
LIST_URL = HOST_URL + "/gzhjs?cb=sogou.weixin.gzhcb&openid={openid}&page={page}"

class SogouWeixinPublicSpider(Spider):
    """usage: scrapy crawl sogou_weixin_public --loglevel=INFO
    """
    name = "sogou_weixin_public"

    def __init__(self):
        self.openid = 'oIWsFt8kxiyiYRj6oWsCQL3hHsqU'
        self.source_website = self.name

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
            source_website = self.source_website
            category = None

            datetime = self.ts2datetime(lastModified.text)

            item_tuple = [key, tplid, classid, docid, title, title1, date, datetime, imglink, headimage, sourcename, content168, isV, openid, content, showurl, url, pagesize, lastModified, source_website, category]
            weixin = ScrapyBoatItem()
            keys = ScrapyBoatItem.RESP_ITER_KEYS_WEIXIN_PUBLIC
            for key in keys:
                item_value = item_tuple[keys.index(key)]
                if item_value and key != "source_website" and key != "datetime":
                    item_value = item_value.text
                elif not item_value:
                    item_value = None
                elif key == "source_website":
                    item_value = item_value
                elif key == "datetime":
                    item_value = item_value
                weixin[key] = item_value

            weixins.append(weixin)

        return weixins

    def get_search_url(self, openid, page):
        return LIST_URL.format(openid=openid, page=page)

    def ts2datetime(self, ts):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
