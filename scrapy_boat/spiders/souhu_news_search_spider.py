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

SEARCH_URL = "http://news.sogou.com/news?query={keyword}&page={page}" # 4表示按照发帖时间排序, 0表示搜索全文, 最多搜825条

class SohuNewsSearchSpider(Spider):
    """usage: scrapy crawl souhu_news_search -a keywords_file='keywords_corp_news.txt'--loglevel=INFO
    """
    name = "souhu_news_search"

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
        search_class = soup.find('div',{'class':'results'})
        search_results = search_class.findAll('div', {'class': 'rb'})
        for result in search_results:
            h3 = result.find('h3')
            if h3:
                h3_a = h3.find('a')
                url = h3_a.get('href')
                title = h3_a.text
                datetime_source_cite = h3.find('cite')
                datetime_source = datetime_source_cite.text
                datetime_source_split = datetime_source.split(';')
                source = datetime_source_split[0]
                datetime_split = datetime_source_split[1].split('r')
                datetime = datetime_split[0]
                log.msg(str(source))
                log.msg(str(datetime))
            ps_div = result.find('div',{'class':'thumb_news'})
            ps = ps_div.find('div',{'class':'ft'})
            # log.msg(str(ps))
            if len(ps):
                summary = ps.text
                same_news_a = ps.find('a')
                # log.msg(str(same_news_a))
                same_news_url = same_news_a.get('href')
                same_news_text = same_news_a.text
                log.msg(str(same_news_text))

                    # &gt;&gt;54条相同新闻
                
                same_news_num = re.search(r'&gt;&gt;(.*?)条相同新闻',same_news_text).group(1)
                log.msg(str(same_news_num))
                timestamp = self.datetimeshort2ts(datetime)
                date = self.ts2date(timestamp)
                source_website = self.source_website
                category = self.category

                news_item = (post_id, title, url, summary, source, timestamp, date, datetime, source_website, category,same_news_url,same_news_num)

                # item = ScrapyBoatItem()
                # keys = ScrapyBoatItem.RESP_ITER_KEYS_TIANYA_BBS
                # for key in keys:
                #     item[key] = news_item[keys.index(key)]
                # results.append(item)

        return results

    def ts2date(self, ts):
        return time.strftime('%Y-%m-%d', time.localtime(ts))

    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

    def datetimeshort2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M')))
