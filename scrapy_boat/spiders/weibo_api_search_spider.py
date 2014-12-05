#-*-coding:utf-8-*-
"""search_spider"""

import time
from scrapy import log
import simplejson as json
from scrapy.http import Request
from scrapy.conf import settings
from scrapy.spider import BaseSpider
from scrapy_boat.items import WeiboItem, UserItem

API_SERVER_HOST = settings.get('API_SERVER_HOST', None)
API_SERVER_PORT = settings.get('API_SERVER_PORT', None)
BASE_URL = 'http://%s:%s/queryWeiboBykw?kw={keywords}&count=50&page={page}' % (API_SERVER_HOST, API_SERVER_PORT)


class WeiboApiSearchSpider(BaseSpider):
    """usage: scrapy crawl weibo_api_search_spider -a keywords_file='keywords_corp_weiboapi.txt' --loglevel=INFO
    """
    name = 'weibo_api_search_spider'

    def __init__(self, keywords_file):
        self.keywords = keywords_file
        self.source_website = self.name
        self.category = keywords_file

    def start_requests(self):
        f = open('./source/' + self.keywords)
        for line in f:
            if '!' in line:
                strip_no_querys = []
                querys = line.strip().lstrip('(').rstrip(')').split(' | ')
                for q in querys:
                    strip_no_querys.append(q.split(' !')[0])
                strip_no_querys = '(' + ' | '.join(strip_no_querys) + ')'
                line = strip_no_querys

            keywords = line.strip().lstrip('(').rstrip(')').split(' | ')
            for keyword in keywords:
                keyword = keyword.split(' ')[0]
                request = Request(BASE_URL.format(keywords=keyword, page=1), headers=None)
                request.meta['page'] = 1
                request.meta['keywords'] = keyword
                yield request

    def parse(self, response):
        page = response.meta['page']
        keywords = response.meta['keywords']

        resp = json.loads(response.body)
        results = []

        for status in resp['statuses']:
            items = self.resp2items(status)
            results.extend(items)

        page += 1
        request = Request(BASE_URL.format(keywords=keywords, page=page), headers=None)
        request.meta['page'] = page
        request.meta['keywords'] = keywords

        results.append(request)

        return results

    def resp2items(self, resp, base_weibo=None, base_user=None):
        items = []
        if resp is None or 'deleted' in resp or 'mid' not in resp and 'name' not in resp:
            return items

        if 'mid' in resp:
            weibo = WeiboItem()
            for key in WeiboItem.RESP_ITER_KEYS:
                if key in resp:
                    weibo[key] = resp[key]
        
            if 'user' not in weibo:
                weibo['user'] = base_user

            weibo['source_website'] = self.source_website
            weibo['source_category'] = self.category
            weibo['timestamp'] = self.local2unix(weibo['created_at'])

            if base_weibo:
                base_weibo['retweeted_status'] = weibo

            items.append(weibo)
            items.extend(self.resp2items(resp.get('user'), base_weibo=weibo))
            items.extend(self.resp2items(resp.get('retweeted_status'), base_weibo=weibo))
        else:
            user = UserItem()
            for key in UserItem.RESP_ITER_KEYS:
                if key in resp:
                    if key == 'class_type':
                        user[key] = resp['class']
                    else:
                        user[key] = resp[key]

            if base_weibo:
                base_weibo['user'] = user

            items.append(user)
            items.extend(self.resp2items(resp.get('status'), base_user=user))

        return items

    def local2unix(self, time_str):
        time_format = '%a %b %d %H:%M:%S +0800 %Y'
        return time.mktime(time.strptime(time_str, time_format))

