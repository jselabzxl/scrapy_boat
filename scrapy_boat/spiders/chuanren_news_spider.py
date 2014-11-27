# -*-coding: utf-8 -*-

import re
import time
import json
from scrapy import log
from scrapy import Spider
from scrapy_boat.items import ChuanrenItem
from scrapy.http import Request
from BeautifulSoup import BeautifulSoup

HOST_URL = "http://www.imarine.cn/"
LIST_URL = HOST_URL + "news.php?typeid=&page={page}"

class ChuanrenNewsSpider(Spider):
    """usage: scrapy crawl chuanren_news --loglevel=INFO
    """
    name = "chuanren_news"

    def __init__(self):
        pass

    def start_requests(self):
        page = 1
        search_url = self.get_search_url(page)
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
        search_url = self.get_search_url(page)
        log.msg(search_url)
        request = Request(search_url)
        request.meta['page'] = page
        results.append(request)

        return results

    def resp2items(self, resp):
        results = []
        soup = BeautifulSoup(resp)
        postlist = soup.find("div", {"class": "postlist module cl xld"})
        posts_dl = postlist.findAll("dl", {"class": "bbdo cl"})
        for post_dl in posts_dl:
            ddm = post_dl.find("dd", {"class": "m"})
            post_url = None
            thumbnail_url = None
            if ddm:
                log.msg(str(ddm))
                post_url = HOST_URL +  ddm.find("a").get("href")
                thumbnail_url = HOST_URL + ddm.find("img").get("src")

            title_dt = post_dl.find("dt")
            title_a = title_dt.find("a")
            post_url = HOST_URL + title_a.get("href")
            post_title = title_a.text

            age_dd = post_dl.find("dd", {"class": "age"})
            if not age_dd:
                age_dd = post_dl.find("dd")
            post_summary = age_dd.text

            xg_dd = post_dl.find("dd", {"class": "xg1 xs1"})
            span_y = xg_dd.find("span", {"class": "y"})
            clicks = int(re.search(r'查看\((.*?)\)&nbsp;', str(span_y)).group(1))
            replies = int(re.search(r'回复\((.*?)\)<', str(span_y)).group(1))

            ddas = xg_dd.findAll("a")
            source_website_name = ddas[0].text
            source_website_url = HOST_URL + ddas[0].get("href")
            source_user_name = ddas[1].text
            source_user_url = HOST_URL + ddas[1].get("href")
            date  = xg_dd.text

            csv_row = (post_url, thumbnail_url, post_title, post_summary, clicks, replies, source_website_name, source_website_url, source_user_name, source_user_url, date)

            item = ChuanrenItem()
            keys = ChuanrenItem.RESP_ITER_KEYS
            for key in keys:
                item[key] = csv_row[keys.index(key)]
            results.append(item)

        return results

    def get_search_url(self, page):
        return LIST_URL.format(page=page)
