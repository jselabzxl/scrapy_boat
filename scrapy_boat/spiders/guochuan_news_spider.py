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
SEARCH_URL = "http://www.eworldship.com/index.php?m=content&c=index&a=lists&catid=821" 

PAGE_URL = "http://www.eworldship.com/index.php?m=content&c=index&a=lists&catid=821&page={page}"

class GuochuanSearchSpider(Spider):
    """usage: scrapy crawl guochuan_news_spider -a start_datetime="2014-11-01 00:00:00" -a end_datetime="2014-12-01 00:00:00" --loglevel=INFO
    """
    name = "guochuan_news_spider"

    def __init__(self, start_datetime, end_datetime):
        self.start_ts = self.datetime2ts(start_datetime)
        self.end_ts = self.datetime2ts(end_datetime)
        self.source_website = self.name

    def start_requests(self):
        page = 1
        search_url = SEARCH_URL.format(page=page)
        request = Request(search_url)
        request.meta['page'] = page

        yield request

    def parse(self, response):
        page = response.meta['page']
        page += 1

        results = []
        resp = response.body

        page_next, items = self.resp2items(resp)
        results.extend(items)

        if page_next:
            search_url = PAGE_URL.format(page=page)
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
        page_next = False
        
        search_list = soup.find('div', {'class': 'col-left'})
        search_ul = search_list.find('ul', {'class': 'content-list'})
        search_results = search_ul.findAll('li')
        for result in search_results:
            span = result.find('span')
            url = None
            thumbnail_url = None
            if span.find("a"):
                span_a = span.find("a")
                url = POST_URL + span_a.get("href")
                thumbnail_url = span_a.find("img").get("src")
            p = result.find("p")
            if p:
                summary = p.text

            h5 = result.find("h5")
            if h5:
                h5_a = h5.find('a')
                short_url = h5_a.get('href')
                url = POST_URL + short_url
                title = h5_a.text 
                id = re.search(r'/html/(.*?).html',short_url).group(1) 
                datetime_span = h5.find("span", {'class': 'f12 fn'})
                datetime_text = datetime_span.text
                datetime = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})', str(datetime_text)).group(1)
                timestamp = self.date2ts(datetime)
                if timestamp > self.start_ts:
                    page_next = True
                date = self.ts2date(timestamp)
            source_website = self.source_website

            news_item = (id, title, url, thumbnail_url, summary, timestamp, date, datetime, source_website)
            item = GuochuanItem()
            keys = GuochuanItem.RESP_ITER_KEYS_GUOCHUAN_NEWS
            for key in keys:
                item[key] = news_item[keys.index(key)]
            results.append(item)

        return page_next, results

    def ts2date(self, ts):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

    def date2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M')))
