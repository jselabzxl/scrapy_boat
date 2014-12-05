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

SEARCH_URL = "http://search.tianya.cn/bbs?q={keyword}&s=4&f=0&pn={page}" # 4表示按照发帖时间排序, 0表示搜索全文, 最多搜825条

class TianyaBbsSearchSpider(Spider):
    """usage: scrapy crawl tianya_bbs_search -a keywords_file='keywords_corp_forum.txt' --loglevel=INFO
    """
    name = "tianya_bbs_search"

    def __init__(self, keywords_file):
        self.keywords = []
        f = open('./source/' + keywords_file)
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
        results = []
        page_next = False
        soup = BeautifulSoup(resp)

        # page
        page_next = False
        long_page = soup.find('div', {'class': 'long-pages'})
        if long_page:
            long_page_as = long_page.findAll('a')
            if len(long_page_as) and long_page_as[-1].text == u'下一页':
                page_next = True

        search_list = soup.find('div', {'class': 'searchListOne'})
        search_results = search_list.findAll('li')
        for result in search_results:
            h3 = result.find('h3')

            if h3:
                h3_a = h3.find('a')
                url = h3_a.get('href')
                post_id = re.search(r'bbs.tianya.cn\/(.*?)\.shtml', url).group(1)
                title = h3_a.text

            ps = result.findAll('p')
            if len(ps):
                summary, source_p = ps
                summary = summary.text
                source_as = source_p.findAll('a')
                source_website_url = source_as[0].get('href')
                source_website_name = source_as[0].text
                user_url = source_as[1].get('href')
                user_name = source_as[1].text

                datetime_replies = source_p.findAll('span')
                datetime, replies = datetime_replies
                datetime = datetime.text
                timestamp = self.datetimeshort2ts(datetime)
                if timestamp < self.start_ts:
                    page_next = False
                replies = replies.text
                source_website = self.source_website
                category = self.category

                bbs_item = (post_id, title, url, summary, source_website_url, source_website_name, user_url, user_name, timestamp, datetime, replies, source_website, category)

                item = ScrapyBoatItem()
                keys = ScrapyBoatItem.RESP_ITER_KEYS_TIANYA_BBS
                for key in keys:
                    item[key] = bbs_item[keys.index(key)]
                results.append(item)

        return page_next, results


    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

    def datetimeshort2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M')))
