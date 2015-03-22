# -*- coding: utf-8 -*-

import re
import time
import json
import sys 
from scrapy import log
from urllib import quote
from scrapy import Spider
from scrapy_boat.items import ZhengyiItem
from scrapy.http import Request
from BeautifulSoup import BeautifulSoup

SEARCH_URL = "http://search.jcrb.com/was5/web/search?page={page}&channelid=19144&searchword={keyword}&keyword={keyword}&perpage=10&outlinepage=10" 

class ZhengyiSearchSpider(Spider):
    """usage: scrapy crawl zhengyi_search -a keywords_file='keywords_zhongchuan.txt' -a start_datetime="2015-02-26 00:00:00" -a end_datetime="2015-03-01 00:00:00" --loglevel=INFO
    """
    name = "zhengyi_search"

    def __init__(self, keywords_file, start_datetime, end_datetime):
        self.keywords = []
        f = open('./source/' + keywords_file)
        for line in f:
            if '!' in line:
                strip_no_querys = []
                querys = line.strip().lstrip('(').rstrip(')').split(' | ')
                for q in querys:
                    strip_no_querys.append(q.split(' !')[0])
                strip_no_querys = '(' + ' | '.join(strip_no_querys) + ')'
                line = strip_no_querys
            keywords_para = quote(line.strip())
            self.keywords.append(keywords_para)
        f.close()

        self.start_ts = self.datetime2ts(start_datetime)
        self.end_ts = self.datetime2ts(end_datetime)
        self.source_website = self.name
        self.category = keywords_file

    def start_requests(self):
        for keyword in self.keywords:
            keyword = "中船重工"
            page = 1
            search_url = SEARCH_URL.format(keyword=keyword, page=page)
            request = Request(search_url)
            request.meta['keyword'] = keyword
            request.meta['page'] = page

            yield request

    def parse(self, response):
        keyword = response.meta['keyword']
        page = response.meta['page']
        page += 1

        results = []
        resp = response.body

        page_next, items = self.resp2items(resp)
        results.extend(items)

        if page_next:
            search_url = SEARCH_URL.format(keyword=keyword, page=page)
            request = Request(search_url)
            request.meta['keyword'] = keyword
            request.meta['page'] = page

            results.append(request)

        return results

    def resp2items(self, resp):
        results = []
        reload(sys)
        sys.setdefaultencoding("utf-8")
        page_next = False
        soup = BeautifulSoup(resp)

        search_list = soup.find('body', {'link': '#261CDC'})
        search_results = search_list.findAll('table')
        for result in search_results:
            tr = result.find('tr')

            if tr.find('td', {'class': 'f'}):
                tr_td = tr.find('td', {'class': 'f'})
                td_font = tr_td.find('font', {'size': '3'})
                td_a = td_font.find('a')
                url = td_a.get('href')
                id = url 
                title = td_a.text

                td_summary = tr_td.find('font', {'size': '-1'})
                font_summary = td_summary.find('font', {'color': '#008000'})
                datetime_author = font_summary.text
                datetime = re.search(r'(.*?)&nbsp;&nbsp; 作者：.*?', str(datetime_author)).group(1)
                summary = td_summary.text

                timestamp = self.datetimeshort2ts(datetime)
                date = self.ts2date(timestamp)
                if timestamp < self.start_ts:
                    page_next = False
                source_website = self.source_website
                category = self.category

                zhengyi_item = (id, title, url, summary, timestamp, date, datetime, source_website, category)
                item = ZhengyiItem()
                keys = ZhengyiItem.RESP_ITER_KEYS_ZHENGYI
                for key in keys:
                    item[key] = zhengyi_item[keys.index(key)]
                results.append(item)

        return page_next, results

    def ts2date(self, ts):
        return time.strftime('%Y-%m-%d', time.localtime(ts))

    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

    def datetimeshort2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y.%m.%d')))
