# -*- coding: utf-8 -*-

import re
import time
import json
from scrapy import log
from urllib import quote
from scrapy import Spider
from scrapy.http import Request
from scrapy_boat.items import ScrapyBoatItem
from BeautifulSoup import BeautifulSoup

HOST_URL = "http://weixin.sogou.com"
LIST_URL = HOST_URL + "/weixin?query={keyword}&type=2&page={page}&ie=utf8&p=01030402&dp=1"


class SogouWeixinSearchSpider(Spider):
    """usage: scrapy crawl sogou_weixin_search -a keywords_file='keywords_corp_weixin.txt' -a start_datetime='2014-11-01 00:00:00' -a end_datetime='2014-12-01 00:00:00' --loglevel=INFO
    """
    name = "sogou_weixin_search"

    def __init__(self, keywords_file, start_datetime, end_datetime):
        self.keywords = []
        f = open('./source/' + keywords_file)
        for line in f:
            if '!' in line:
                strip_no_querys = []
                querys = line.strip().lstrip('(').rstrip(')').split(' | ')
                for q in querys:
                    strip_no_querys.append(q.split(' !')[0])
                strip_no_querys = '+'.join(strip_no_querys)
                line = strip_no_querys
            keywords_para = line.strip().lstrip('(').rstrip(')').split(' | ')
            self.keywords.extend(keywords_para)
        f.close()

        self.page_count = 100
        self.start_ts = self.datetime2ts(start_datetime)
        self.end_ts = self.datetime2ts(end_datetime)
        self.source_website = self.name
        self.category = keywords_file

    def start_requests(self):
        page = 1
        for keyword in self.keywords:
            search_url = self.get_search_url(keyword, page)
            request = Request(search_url)
            request.meta['page'] = page
            request.meta['keyword'] = keyword

            yield request

    def parse(self, response):
        results = []
        page = response.meta['page']
        keyword = response.meta['keyword']

        resp = response.body
        page_next, items = self.resp2items(resp)
        results.extend(items)

        if page_next:
            page += 1
            search_url = self.get_search_url(keyword, page)
            request = Request(search_url)
            request.meta['page'] = page
            request.meta['keyword'] = keyword
            results.append(request)

        return results

    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

    def ts2date(self, ts):
        return time.strftime('%Y-%m-%d', time.localtime(ts))

    def ts2datetime(self, ts):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

    def resp2items(self, resp):
        weixins = []
        resp = resp.replace("red_beg", "").replace("red_end", "").replace("&mdash;", "")
        soup = BeautifulSoup(resp)
        wx_rbs = soup.findAll("div", {"class": "wx-rb wx-rb3"})

        page_next = False

        for wx_rb in wx_rbs:
            post_id = wx_rb.get("d")

            img_box = wx_rb.find("div", {"class": "img_box2"})
            post_url = img_box.find("a").get("href")
            post_img = img_box.find("a").find("img").get("src")

            txt_box = wx_rb.find("div", {"class": "txt-box"})
            post_title = txt_box.find("h4").find("a").text
            post_url = txt_box.find("h4").find("a").get("href")
            post_summary = txt_box.find("p").text
            s_p_div = txt_box.find("div", {"class": "s-p"})
            s_p_a = s_p_div.find("a")
            post_source_url = HOST_URL + s_p_a.get("href")
            post_source_name = s_p_a.get("title")
            timestamp = int(s_p_div.get("t"))
            if timestamp < self.start_ts:
                page_next = False
            date = self.ts2date(timestamp)
            datetime = self.ts2datetime(timestamp)
            source_website = self.source_website
            category = self.category

            item_tuple = [post_id, post_img, post_title, post_url, \
                    post_summary, post_source_url, post_source_name, \
                    timestamp, date, datetime, source_website, category]
            weixin = ScrapyBoatItem()
            keys = ScrapyBoatItem.RESP_ITER_KEYS_WEIXIN_SEARCH
            for key in keys:
                item_value = item_tuple[keys.index(key)]
                if item_value:
                    item_value = item_value
                else:
                    item_value = None
                weixin[key] = item_value

            weixins.append(weixin)

        return page_next, weixins

    def get_search_url(self, keyword, page):
        return LIST_URL.format(keyword=keyword, page=page)

