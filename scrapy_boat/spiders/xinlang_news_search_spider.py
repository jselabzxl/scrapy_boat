# -*- coding: utf-8 -*-

import re
import time
import json
import sys
from scrapy import log
from urllib import quote
from urllib import unquote
from scrapy import Spider
from scrapy_boat.items import ScrapyBoatItem
from scrapy.http import Request
from BeautifulSoup import BeautifulSoup

SEARCH_URL = "http://search.sina.com.cn/?c=news&q={keyword}&range=all&time=2014&stime=&etime=&num=20&col=&source=&from=&country=&size=&a=&page={page}&pf=2131490986&ps=2134309112&dpc=1" # 4表示按照发帖时间排序, 0表示搜索全文, 最多搜825条

class XinlangNewsSearchSpider(Spider):
    """usage: scrapy crawl xinlang_news_search -a keywords_file='keywords_corp_news.txt'--loglevel=INFO
    """
    name = "xinlang_news_search"

    def __init__(self, keywords_file):
        self.keywords = []
        f = open(keywords_file)
        for line in f:
            if '!' in line:
                strip_no_querys = []
                querys = line.strip().lstrip('(').rstrip(')').split(' | ')
                for q in querys:
                    strip_no_querys.append(q.split(' !')[0])
                strip_no_querys = ' '.join(strip_no_querys)
                line = strip_no_querys
            keywords_para = line.strip().lstrip('(').rstrip(')').split(' | ')
            self.keywords.extend(keywords_para)
        f.close()

        # self.start_ts = self.datetime2ts(start_datetime)
        # self.end_ts = self.datetime2ts(end_datetime)
        # self.source_website = self.name
        self.category = keywords_file

    def start_requests(self):
        for keyword in self.keywords:
            page = 1
            search_url = SEARCH_URL.format(keyword=keyword, page=page)
            log.msg(search_url)
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

        items = self.resp2items(resp)
        results.extend(items)
        log.msg(str(results))
        # if page_next:
        #     search_url = SEARCH_URL.format(keyword=keyword, page=page)
        #     log.msg(search_url)
        #     request = Request(search_url)
        #     request.meta['keyword'] = keyword
        #     request.meta['page'] = page

        #     results.append(request)

        return results

    def resp2items(self, resp):
        reload(sys)  
        sys.setdefaultencoding('utf8')
        results = []
        page_next = False
        soup = BeautifulSoup(resp)
        # page
        # page_next = False
        # scrollDiv = soup.find('div', {'class': 'scrollDiv'})
        # if long_page:
        #     long_page_as = long_page.findAll('a')
        #     if len(long_page_as) and long_page_as[-1].text == u'下一页':
        #         page_next = True

        search_results = soup.findAll('div', {'class': 'box-result clearfix'})
        for result in search_results:
            h2 = result.find('h2')
            if h2:
                h2_a = h2.find('a')
                url = h2_a.get('href')
                title = h2_a.text

            source_website_span = result.find('span',{'class':'fgray_time'})
            log.msg(str(source_website_span))
            datetime_source = str(source_website_span)
            # <span class="fgray_time">新浪财经 2014-12-24 17:57:36</span>
            source = re.search(r'<span class="fgray_time">(.*?)\d{1,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}</span>', datetime_source).group(1)
            datetime = re.search(r'<span class="fgray_time">.*?(\d{1,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})</span>', datetime_source).group(1)
            log.msg(str(source))
            log.msg(str(datetime))
            ps = result.find('p',{'class':'content'})
            if len(ps):
                summary = ps.text
                log.msg(str(summary))
                timestamp = self.datetimeshort2ts(datetime)
                date = self.ts2date(timestamp)
                # if timestamp < self.start_ts:
                #     page_next = False
                source_website = self.source_website
                category = self.category

                news_item = (post_id, title, url, summary, source, timestamp, date, datetime, source_website, category)

                # item = ScrapyBoatItem()
                # keys = ScrapyBoatItem.RESP_ITER_KEYS_TIANYA_BBS
                # for key in keys:
                #     item[key] = news_item[keys.index(key)]
                # results.append(item)

        return page_next, results

    def ts2date(self, ts):
        return time.strftime('%Y-%m-%d', time.localtime(ts))

    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

    def datetimeshort2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))
