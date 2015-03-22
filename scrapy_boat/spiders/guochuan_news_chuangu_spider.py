# -*- coding: utf-8 -*-

import re
import time
import json
import sys
from scrapy import log
from urllib import quote
from scrapy import Spider
from scrapy_boat.items import GuochuanItem
from scrapy.http import Request
from BeautifulSoup import BeautifulSoup

POST_URL = "http://www.eworldship.com"
SEARCH_URL = "http://www.eworldship.com/app/news/listview?id=MDAwMDAwMDAwMLF8eds&channel=MDAwMDAwMDAwMJl9g52ZaLzT&page=MDAwMDAwMDAwMISCdXM" 

class GuochuanSearchSpider(Spider):
    """usage: scrapy crawl guochuan_news_chuangu_spider -a start_datetime="2014-11-01 00:00:00" -a end_datetime="2014-12-01 00:00:00" --loglevel=INFO
    """
    name = "guochuan_news_chuangu_spider"

    def __init__(self, start_datetime, end_datetime):
        self.start_ts = self.datetime2ts(start_datetime)
        self.end_ts = self.datetime2ts(end_datetime)
        self.source_website = "guochuan_news_chuangu_spider"

    def start_requests(self):
        request = Request(SEARCH_URL)
        yield request

    def parse(self, response):
        results = []
        resp = response.body
        items = self.resp2items(resp)
        results.extend(items)
        return results

    def resp2items(self, resp):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        results = []
        soup = BeautifulSoup(resp)
        
        search_list = soup.find('div', {'class': 'area'})
        search_div = search_list.find('div', {'class': 'area-left'})
        search_results = search_div.findAll('div', {'class': 'list-item clearfix'})
        for result in search_results:
            item_top = result.find('div', {'class': 'item-top'})
            url = None  
            thumbnail_url = None
            h2 = item_top.find("h2")
            h2_a = h2.find("a")
            short_url = h2_a.get("href")
            id = re.search(r'/html/(.*?).html',short_url).group(1) 
            title = h2_a.text
            url = POST_URL + short_url
            p = item_top.find("p")
            if p:
                summary = p.text

            h5 = p.find('span', {'class': 'time'})
            if h5:
                datetime = h5.text
                timestamp = self.datetime2ts(datetime)
                date = self.ts2date(timestamp)
            source_website = self.source_website

            news_item = (id, title, url, thumbnail_url, summary, timestamp, date, datetime, source_website)
            item = GuochuanItem()
            keys = GuochuanItem.RESP_ITER_KEYS_GUOCHUAN_NEWS
            for key in keys:
                item[key] = news_item[keys.index(key)]
            results.append(item)

        return results

    def ts2date(self, ts):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

    def date2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M')))
