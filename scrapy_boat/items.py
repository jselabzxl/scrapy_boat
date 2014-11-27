# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyBoatItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    same_news_num = scrapy.Field()
    more_same_link = scrapy.Field()
    relative_news = scrapy.Field()
    author = scrapy.Field()
    datetime = scrapy.Field()
    summary = scrapy.Field()

    RESP_ITER_KEYS = ['title', 'url', 'same_news_num', 'more_same_link', 'relative_news', 'author', 'datetime', 'summary']

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (ScrapyBoatItem)):
                d[k] = v.to_dict()
            else:
                d[k] = v

        return d

class WeixinItem(scrapy.Item):
    key = scrapy.Field()
    tplid = scrapy.Field()
    classid = scrapy.Field()
    docid = scrapy.Field()
    title = scrapy.Field()
    title1 = scrapy.Field()
    date = scrapy.Field()
    imglink = scrapy.Field()
    headimage = scrapy.Field()
    sourcename = scrapy.Field()
    content168 = scrapy.Field()
    isV = scrapy.Field()
    openid = scrapy.Field()
    content = scrapy.Field()
    showurl = scrapy.Field()
    url = scrapy.Field()
    pagesize = scrapy.Field()
    lastModified = scrapy.Field()

    RESP_ITER_KEYS = ['key', 'tplid', 'classid', 'docid', 'title', 'title1', 'date', 'imglink', 'headimage', 'sourcename', 'content168', 'isV', 'openid', 'content', 'showurl', 'url', 'pagesize', 'lastModified']

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (WeixinItem)):
                d[k] = v.to_dict()
            else:
                d[k] = v

        return d

class ChuanrenItem(scrapy.Item):
    post_url = scrapy.Field()
    thumbnail_url = scrapy.Field()
    post_title = scrapy.Field()
    post_summary = scrapy.Field()
    clicks = scrapy.Field()
    replies = scrapy.Field()
    website_name = scrapy.Field()
    website_url = scrapy.Field()
    user_name = scrapy.Field()
    user_url = scrapy.Field()
    date = scrapy.Field()

    RESP_ITER_KEYS = ['post_url', 'thumbnail_url', 'post_title', 'post_summary', 'clicks', 'replies', 'website_name', 'website_url', 'user_name', 'user_url', 'date']

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (ChuanrenItem)):
                d[k] = v.to_dict()
            else:
                d[k] = v

        return d
