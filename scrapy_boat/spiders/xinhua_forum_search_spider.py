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


SEARCH_URL = "http://search.home.news.cn/forumbookSearch.do?title=&adv=1&content={keyword}&nickName=&bid=0&start={start_datetimeshort}&end={end_datetimeshort}&pageSize=400&pageNo={page}"


class XinhuaBbsSearchSpider(Spider):
    """usage: scrapy crawl xinhua_bbs_search -a keywords_file='keywords_corp_forum.txt' -a start_datetime="2014-11-01 00:00:00" -a end_datetime="2014-12-01 00:00:00" --loglevel=INFO
    """
    name = "xinhua_bbs_search"

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
            keywords_para = line.strip()
            self.keywords.append(keywords_para)
        f.close()

        self.start_ts = self.datetime2ts(start_datetime)
        self.end_ts = self.datetime2ts(end_datetime)
        self.start_datetimeshort = quote(self.ts2datetimeshort(self.start_ts))
        self.end_datetimeshort = quote(self.ts2datetimeshort(self.end_ts))
        self.source_website = self.name
        self.category = keywords_file

    def start_requests(self):
        for keyword in self.keywords:
            page = 1
            search_url = SEARCH_URL.format(keyword=keyword, page=page, start_datetimeshort=self.start_datetimeshort, end_datetimeshort=self.end_datetimeshort)
            log.msg(search_url)
            request = Request(search_url)
            request.meta['keyword'] = keyword
            request.meta['page'] = page
            request.meta['start'] = self.start_datetimeshort
            request.meta['end'] = self.end_datetimeshort

            yield request

    def parse(self, response):
        keyword = response.meta['keyword']
        page = response.meta['page']
        start = response.meta['start']
        end = response.meta['end']

        results = []
        resp = response.body

        page_next, items = self.resp2items(resp, page)
        results.extend(items)

        if page_next:
            page += 1
            search_url = SEARCH_URL.format(keyword=keyword, page=page, start_datetimeshort=start, end_datetimeshort=end)
            log.msg(search_url)
            request = Request(search_url)
            request.meta['keyword'] = keyword
            request.meta['page'] = page
            request.meta['start'] = start
            request.meta['end'] = end

            results.append(request)

        return results

    def resp2items(self, resp, page):
        results = []
        soup = BeautifulSoup(resp)

        # page
        page_next = False
        total_page = 0
        long_page = soup.find('td', {'class': 'xg12'})
        if long_page:
            total_page = int(long_page.findAll('font', {'color': '#e38311'})[-1].text)

        if page < total_page:
            page_next = True

        search_list = soup.find('div', {'style': 'text-align: center'})
        search_table = search_list.find('table', {'align': 'center'})
        search_results = search_table.findAll('div', {'id': 'schend'})
        for result in search_results:
            table = result.findAll('table')

            td = table[0].find('td', {'width':'614'})
            td_a = td.find('a')
            url = td_a.get('href')
            post_id = "xinhua_forum_" + re.search(r'Single.do\?id=(.*?)\&ui', url).group(1)
            title = td_a.text

            td2 = table[0].find('td', {'width': '135'})
            td2_a = td2.find('a')
            user_name = td2_a.find('span', {'class': 'sk'}).text
            user_url = td2_a.get('href')

            td3 = table[0].find('td', {'width': '150'})
            datetime = td3.text
            timestamp = self.datetime2ts(datetime)

            summary = table[2].find('td')
            summary = summary.text

            source_website = self.source_website
            category = self.category

            bbs_item = (post_id, title, url, summary, user_url, user_name, timestamp, datetime, source_website, category)

            item = ScrapyBoatItem()
            keys = ScrapyBoatItem.RESP_ITER_KEYS_XINHUA_BBS
            for key in keys:
                item[key] = bbs_item[keys.index(key)]
            results.append(item)

        return page_next, results

    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

    def ts2datetimeshort(self, ts):
        return time.strftime('%Y-%m-%d %H:%M',time.localtime(ts))

