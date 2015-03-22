# -*-coding: utf-8 -*-

import re
import time
import json
import sys
from scrapy import log
from scrapy import Spider
from scrapy_boat.items import ChuanrenItem
from scrapy.http import Request
from BeautifulSoup import BeautifulSoup

HOST_URL = "http://www.imarine.cn/"
LIST_URL = HOST_URL + "news.php?typeid=&page={page}"

class ChuanrenNewsSpider(Spider):
    """usage: scrapy crawl chuanren_news_spider -a start_datetime="2014-11-01 00:00:00" -a end_datetime="2014-12-01 00:00:00" --loglevel=INFO
    """
    name = "chuanren_news_spider"

    def __init__(self, start_datetime, end_datetime):
        self.start_ts = self.datetime2ts(start_datetime)
        self.end_ts = self.datetime2ts(end_datetime)
        self.source_website = self.name
        pass

    def start_requests(self):
        page = 1
        search_url = self.get_search_url(page)
        request = Request(search_url)
        request.meta['page'] = page

        yield request

    def parse(self, response):
        results = []

        resp = response.body
        page_next, items = self.resp2items(resp)
        results.extend(items)


        page = response.meta['page']
        page += 1

        if page_next:
            search_url = self.get_search_url(page)
            request = Request(search_url)
            request.meta['page'] = page
            results.append(request)

        return results

    def resp2items(self, resp):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        results = []
        page_next = False
        soup = BeautifulSoup(resp)
        postlist = soup.find("div", {"class": "postlist module cl xld"})
        posts_dl = postlist.findAll("dl", {"class": "bbdo cl"})
        for post_dl in posts_dl:
            ddm = post_dl.find("dd", {"class": "m"})
            url = None
            thumbnail_url = None
            if len(str(ddm)) > 20:
                url = HOST_URL +  ddm.find("a").get("href")
                thumbnail_url = HOST_URL + ddm.find("img").get("src")

            title_dt = post_dl.find("dt")
            title_a = title_dt.find("a")
            id_string = title_a.get("href")
            id = re.search(r'(.*?).html', id_string).group(1)
            url = HOST_URL + title_a.get("href")
            title = title_a.text

            age_dd = post_dl.find("dd", {"class": "age"})
            if not age_dd:
                age_dd = post_dl.find("dd")
            summary = age_dd.text

            xg_dd = post_dl.find("dd", {"class": "xg1 xs1"})
            span_y = xg_dd.find("span", {"class": "y"})
            clicks = int(re.search(r'查看\((.*?)\)&nbsp;', str(span_y)).group(1))
            replies = int(re.search(r'回复\((.*?)\)<', str(span_y)).group(1))

            ddas = xg_dd.findAll("a")
            source_website_name = ddas[0].text
            source_website_url = HOST_URL + ddas[0].get("href")
            source_user_name = ddas[1].text
            source_user_url = HOST_URL + ddas[1].get("href")
            split  = xg_dd.text.split("|")
            datetime = split[2]
            timestamp = self.date2ts(datetime)
            if timestamp > self.start_ts:
                page_next = True
            date = self.ts2date(timestamp)
            source_website = self.source_website

            csv_row = (id, url, thumbnail_url, title, summary, clicks, replies, source_website_name, source_website_url, source_user_name, source_user_url, datetime, timestamp, date, source_website)
            item = ChuanrenItem()
            keys = ChuanrenItem.RESP_ITER_KEYS_CHUANREN_NEWS
            for key in keys:
                item[key] = csv_row[keys.index(key)] 
            results.append(item)
        return  page_next, results

    def get_search_url(self, page):
        return LIST_URL.format(page=page)


    def date2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d')))

    def ts2date(self, ts):
        return time.strftime('%Y-%m-%d', time.localtime(ts))

    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))