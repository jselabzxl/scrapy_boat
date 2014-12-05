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

def ts2date(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

class SogouWeixinSearchSpider(Spider):
    """usage: scrapy crawl sogou_weixin_search -a keywords_file='keywords_corp_weixin.txt' --loglevel=INFO
    """
    name = "sogou_weixin_search"

    def __init__(self, keywords_file):
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
        self.start_ts = self.datetime2ts('2014-11-01 00:00:00')
        self.end_ts = self.datetime2ts('2014-12-01 00:00:00')
        self.source_website = self.name
        self.category = keywords_file

    def start_requests(self):
        page = 1
        for keyword in self.keywords:
            search_url = self.get_search_url(keyword, page)
            log.msg(search_url)
            request = Request(search_url)
            request.meta['page'] = page
            request.meta['keyword'] = keyword

            yield request

    def parse(self, response):
        results = []

        resp = response.body
        items = self.resp2items(resp)
        results.extend(items)

        page = response.meta['page']
        keyword = response.meta['keyword']
        page += 1
        search_url = self.get_search_url(keyword, page)
        log.msg(search_url)
        request = Request(search_url)
        request.meta['page'] = page
        request.meta['keyword'] = keyword
        results.append(request)

        return results

    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

    def resp2items(self, resp):
        weixins = []
        resp = resp.replace("red_beg", "").replace("red_end", "").replace("&mdash;", "")
        soup = BeautifulSoup(resp)
        wx_rbs = soup.findAll("div", {"class": "wx-rb wx-rb3"})
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
            date = ts2date(timestamp)
            source_website = self.source_website
            category = self.category

            item_tuple = [post_id, post_img, post_title, post_url, post_summary, post_source_url, post_source_name, timestamp, date, source_website, category]
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

        return weixins

    def get_search_url(self, keyword, page):
        return LIST_URL.format(keyword=keyword, page=page)

