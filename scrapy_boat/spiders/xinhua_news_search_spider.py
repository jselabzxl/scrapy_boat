# -*- coding: utf-8 -*-

import re
import time
import json
from scrapy import log
from urllib import quote
from scrapy import Spider
from scrapy_boat.items import ScrapyBoatItem
from scrapy.http import Request
from BeautifulSoup import BeautifulSoup

# SEARCH_URL = "http://search.tianya.cn/bbs?q={keyword}&s=4&f=0&pn={page}" # 4表示按照发帖时间排序, 0表示搜索全文, 最多搜825条
SEARCH_URL = "http://info.search.news.cn/result.jspa?pno={page}&rp=10&t1=0&btn=&t=1&n1={keyword}&np=1&ss=2"
class XinhuaNewsSearchSpider(Spider):
    """usage: scrapy crawl xinhua_news_search -a keywords_file='keywords_corp_news.txt' --loglevel=INFO
    """
    name = "xinhua_news_search"

    def __init__(self, keywords_file):
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

        self.start_ts = self.datetime2ts('2014-11-01 00:00:00')
        self.end_ts = self.datetime2ts('2014-12-01 00:00:00')
        self.source_website = self.name
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

        page_next, items = self.resp2items(resp)
        results.extend(items)

        if page_next:
            search_url = SEARCH_URL.format(keyword=keyword, page=page)
            log.msg(search_url)
            request = Request(search_url)
            request.meta['keyword'] = keyword
            request.meta['page'] = page

            results.append(request)

        return results

    def resp2items(self, resp):
        page_next = False
        results = []
        soup = BeautifulSoup(resp)

        # page
        # long_page = soup.find('div', {'class': 'long-pages'})
        # if long_page 

        search_list = soup.find('div', {'class': 'middle-c'})
        search_results = search_list.findAll('div', {'align': 'left'})
        for result in search_results:
            span = result.find('span',{'class':'style1d'})
            if span:
                span_a = span.find('a')
                url = span_a.get('href')
                log.msg(url)
                # post_id = re.search(r'bbs.tianya.cn\/(.*?)\.shtml', url).group(1)
                # post_id = re.search(r'http://news.xinhuanet.com/comments\/(.*?)\.htm', url).group(1)
                split_underline = url.split('_')
                split_point = split_underline[1].split('.')
                post_id = split_point[0]
                title = span_a.text

            source_datatime = result.find('span',{'class':'style2a'})
            if source_datatime:
                split_space = source_datatime.split('  ')
                source = split_space[0]
                datetime = split_space[1]
                timestamp = self.datetimeshort2ts(datetime)

            summary = result.find('span',{'class':'cc'})
            if len(summary):
                summary = summary.text
                # source_as = source_p.findAll('a')
                # source_website_url = source_as[0].get('href')
                # source_website_name = source_as[0].text
                # user_url = source_as[1].get('href')
                # user_name = source_as[1].text

                # datetime_replies = source_p.findAll('span')
                # datetime, replies = datetime_replies
                # datetime = datetime.text
                # timestamp = self.datetimeshort2ts(datetime)
                # replies = replies.text
                source_website = self.source_website
                category = self.category
                xinhua_item = (post_id, title, url, source, summary, timestamp, datetime,source_website,category)
                item = ScrapyBoatItem()
                keys = ScrapyBoatItem.RESP_ITER_KEYS_XINHUA_NEWS
                for key in keys:
                    item[key] = xinhua_item[keys.index(key)]
                results.append(item)

        return results


    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

    def datetimeshort2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d')))
