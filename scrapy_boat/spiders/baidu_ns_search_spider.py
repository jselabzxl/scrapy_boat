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

HOST_URL = "http://news.baidu.com"
LIST_URL = HOST_URL + "/ns?word={topic}&pn={offset}&cl=2&ct=1&tn=newsdy&rn={page_count}&ie=utf-8&bt={start_ts}&et={end_ts}"

class BaiduNsSearchSpider(Spider):
    """usage: scrapy crawl baidu_ns_search -a keywords_file='keywords_corp.txt' --loglevel=INFO
    """
    name = "baidu_ns_search"

    def __init__(self, keywords_file):
        self.keywords = []
        f = open('./keywords/' + keywords_file)
        for line in f:
            keywords_para = quote(line.strip())
            self.keywords.append(keywords_para)
        f.close()

        self.page_count = 100
        self.start_ts = self.datetime2ts('2014-11-01 00:00:00')
        self.end_ts = self.datetime2ts('2014-11-22 00:00:00')

    def start_requests(self):
        for keyword in self.keywords:
            search_url = self.get_search_url(0, keyword, self.start_ts, self.end_ts, self.page_count)
            log.msg(search_url)
            request = Request(search_url)

            yield request

    def parse(self, response):
        # 解析搜索结果列表页面
        results = []
        resp = response.body
        if 'relative_news' in response.meta:
            item = response.meta['relative_news']
        else:
            item = None

        hits, return_items, requests = self.resp2items(resp, base_item=item)
        results.extend(return_items)
        results.extend(requests)

        return results

    def parse_more(self, response):
        # 解析相关新闻页面
        results = []
        resp = response.body
        item = response.meta['relative_news']

        hits, return_items, requests = self.resp2items(resp, base_item=item)
        item['same_news_num'] = hits
        results.append(item)
        results.extend(return_items)

        return results

    def get_search_url(self, offset, topic, start_ts, end_ts, page_count=100):
        return LIST_URL.format(topic=topic, offset=offset, page_count=page_count, start_ts=start_ts, end_ts=end_ts)

    def datetime2ts(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

    def resp2items(self, resp, base_item=None):
        soup = BeautifulSoup(resp)

        # hits
        hits = 0
        nums_span = soup.find('span', {'class': 'nums'})
        if nums_span:
            hits = int(re.search(r'闻(.*?)篇', nums_span.text.encode('utf-8')).group(1).replace('约', '').decode('utf8').replace(',', ''))

        # items
        items = []
        content_left = soup.find('div', {'id': 'content_left'})
        if content_left:
            result_lis = content_left.findAll('li', {'class': 'result'})
            for li in result_lis:
                title = li.find('h3', {'class': 'c-title'}).find('a').text
                url = li.find('h3', {'class': 'c-title'}).find('a').get('href')

                summary_div = li.find('div', {'class': 'c-summary c-row '})
                if not summary_div:
                    summary_div = li.find('div', {'class': 'c-summary c-row c-gap-top-small'})

                author_div = summary_div.find('p', {'class': 'c-author'})
                author = str(author_div).split('&nbsp;&nbsp;')[0].strip('<p class="c-author">').decode('utf-8')
                datetime = str(author_div).split('&nbsp;&nbsp;')[1].strip('</p>').replace('  ', ' ')
                summary = re.search(r'</p>(.*?)<a', str(summary_div)).group(1).decode('utf-8').replace('<em>', '').replace('</em>', '')

                more_same_link = None
                c_more_link_a =  summary_div.find('a', {'class': 'c-more_link'})
                if c_more_link_a:
                    more_same_link = HOST_URL + c_more_link_a.get('href')
                same_news_num = 0
                relative_news = None

                news_item = {'title': title, 'url': url, 'same_news_num': same_news_num, 'more_same_link': more_same_link, 'relative_news': relative_news, 'author': author, 'datetime': datetime, 'summary': summary}

                item = ScrapyBoatItem()
                for key in ScrapyBoatItem.RESP_ITER_KEYS:
                    item[key] = news_item[key]

                if base_item:
                    item['relative_news'] = base_item

                items.append(item)

        # requests and return_items
        requests = []
        return_items = []
        for item in items:
            if item['more_same_link']:
                request = Request(item['more_same_link'], callback=self.parse_more)
                request.meta['relative_news'] = item
                requests.append(request)
            else:
                return_items.append(item)

        page_p = soup.find('p', {'id': 'page'})
        if page_p:
            n_as = page_p.findAll('a', {'class': 'n'})
            if len(n_as) > 0:
                if n_as[-1].text.replace('&gt;', '') == u'下一页':
                    search_url = HOST_URL + n_as[-1].get('href')
                    log.msg(search_url)
                    request = Request(search_url, callback=self.parse)
                    if base_item:
                        request.meta['relative_news'] = base_item

                    requests.append(request)

        return hits, return_items, requests

