
# -*-coding: utf-8 -*-

import re
import time
import json
import sys
from scrapy import log
from scrapy import Spider
from scrapy_boat.items import ScrapyRenwuItem
from scrapy.http import Request
from BeautifulSoup import BeautifulSoup


url_list = ["http://www.cnss.com.cn/html/finance/hyrw/{page}.html"]
RENWU_NEWS_KEYS = {'id':None , 'url':None, 'thumbnail_url':None, 'title':None, 'summary':None, 'clicks':None, 'replies':None, 'website_name':None, 'website_url':None, 'user_name':None, 'user_url':None, 'tag':None, 'datetime':None, 'timestamp':None, 'date':None, 'source_website':None}

class HaishiNewsSpider(Spider):
    """usage: scrapy crawl haishi_renwu_spider -a start_datetime="2014-11-01 00:00:00" -a end_datetime="2014-12-01 00:00:00" --loglevel=INFO
    """
    name = "haishi_renwu_spider"
    
    def __init__(self, start_datetime, end_datetime):
        self.start_ts = self.datetime2ts(start_datetime)
        self.end_ts = self.datetime2ts(end_datetime)
        self.source_website = self.name

    def start_requests(self):
        for url in url_list:
            page = 'index'
            request = Request(url.format(page=page))
            request.meta['page'] = page
            request.meta['url'] = url
            yield request

    def parse(self, response):
        url = response.meta['url']
        page = response.meta['page']

        results = []
        resp = response.body
        page_next, items = self.resp2items(resp)
        results.extend(items)

        if page != 'index': 
            page += 1
        else:
            page = 2

        if page_next:
            request = Request(url.format(page=page))
            request.meta['page'] = page
            request.meta['url'] = url
            results.append(request)

        return results

    def resp2items(self, resp):
        page = 1
        reload(sys)
        sys.setdefaultencoding("utf-8")
        results = []
        page_next = False
        soup = BeautifulSoup(resp)
        postbody = soup.find("div", {"class": "bodyLeft"})
        postlist = postbody.findAll("div", {"class": "newsList"})
        for post_news in postlist:
            pic = post_news.find("div", {"class": "pic"})
            url = None
            thumbnail_url = None
            if pic:
                pic_a = pic.find("a")
                url = pic_a.get("href")
                thumbnail_url = pic_a.find("img").get("src")

            title_info = post_news.find("div", {"class": "infoDoc"})
            title_h1 = title_info.find("h1")
            title_a = title_h1.find("a")
            id_string = title_a.get("href")
            id = re.search(r'http://www.cnss.com.cn/html/(.*?).html', id_string).group(1)
            url = title_a.get("href")
            title = title_a.text

            info = title_info.find("div", {"class": "info"})
            summary = info.text

            h2 = title_info.find("h2")
            h2_span = h2.find("span")
            replies = int(re.search(r'评论\((.*?)\)<', str(h2_span)).group(1))

            h2_b = h2.find("b")
            datetime_text = h2_b.text
            datetime = re.search(r'(.*?)&nbsp;&nbsp;标签', str(datetime_text)).group(1)
            tag = []
            tag_a = h2_b.findAll("a")
            for k in tag_a:
                tag.append((k.text).encode('utf-8'))
            timestamp = self.date2ts(datetime)
            if timestamp > self.start_ts:
                page_next = True
            date = self.ts2date(timestamp)
            source_website = self.source_website

            csv_row = (id, url, thumbnail_url, title, summary, replies, tag, datetime, timestamp, date, source_website)
            item = ScrapyRenwuItem()
            keys = ScrapyRenwuItem.RESP_ITER_KEYS_HAISHI_NEWS
            for key in RENWU_NEWS_KEYS: 
                RENWU_NEWS_KEYS[key] = None
                item[key] = RENWU_NEWS_KEYS[key]
            for key in keys:
                item[key] = csv_row[keys.index(key)] 
            results.append(item)
            print item
        return  page_next, results

    def date2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d')))

    def ts2date(self, ts):
        return time.strftime('%Y-%m-%d', time.localtime(ts))

    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))