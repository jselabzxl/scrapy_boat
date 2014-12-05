# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ScrapyBoatItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field() # 原文标题,【新闻速递】亚洲造船专家齐聚韩国济州岛  \u2014\u2014第八届亚...
    url = scrapy.Field() # 原文链接
    summary = scrapy.Field() # 文本概述
    timestamp = scrapy.Field() # 时间戳，自1970-1-1的秒数
    datetime = scrapy.Field() # 2011-02-21 17:35:47
    date = scrapy.Field() # 2014-11-28
    thumbnail_url = scrapy.Field() # 缩略图url
    user_id = scrapy.Field() # 用户id
    user_url = scrapy.Field() # 用户url
    user_image_url = scrapy.Field() # 用户头像url, 公众平台帐号头像url, http://wx.qlogo.cn/mmhead/Q3auHgzwzM4Ot2SWhTdlicTICNicOH9fgDAicuX16sYicPCZDle7aicxvcQ/0
    user_name = scrapy.Field() # 用户名, 公众帐号名, 中船重工经济研究中心
    source_website = scrapy.Field() # 来源渠道
    category = scrapy.Field() # 信息类别

    # baidu
    same_news_num = scrapy.Field() # 相同新闻数
    more_same_link = scrapy.Field() # 相同新闻链接
    relative_news = scrapy.Field() # 关联的新闻

    # weixin public
    key = scrapy.Field() # http://mp.weixin.qq.com/
    tplid = scrapy.Field() # 550
    classid = scrapy.Field() # 11002601
    # docid = scrapy.Field() # document id ,用id字段替换, ab735a258a90e8e1-6bee54fcbd896b2a-964b1fa79f51be4294b2819a08235c0a
    title1 = scrapy.Field() # 【新闻速递】亚洲造船专家齐聚韩国济州岛  \u2014\u2014第八届亚洲造船专家技术论坛(ASEF)
    content168 = scrapy.Field()
    isV = scrapy.Field() # 1
    # openid = scrapy.Field() # 公众帐号id, 用user_id替换, oIWsFt8kxiyiYRj6oWsCQL3hHsqU
    # content = scrapy.Field() # 用summary代替, 点击上方\u201c蓝色字体\u201d可以订阅哦!亚洲造船专家齐聚韩国济州岛\u2014\u2014第八届亚洲造船专家技术论坛(ASEF) 2014年11月27日-28日...
    showurl = scrapy.Field() # 微信 - mp.weixin.qq.com
    pagesize = scrapy.Field() # 31k
    # lastModified = scrapy.Field() # 最后修改时间戳，用timestamp的替换

    # weixin search
    # post_id = scrapy.Field() # document id ,用id字段替换, ab735a258a90e8e1-6bee54fcbd896b2a-7fa89f251bc5802b223ed97b15bb48d4

    #tianya bbs
    source_from_url = scrapy.Field() # 帖子来源版块url
    source_from_name = scrapy.Field() # 帖子来源版块名称
    replies = scrapy.Field() # 回复数

    RESP_ITER_KEYS_BAIDU = ['title', 'url', 'same_news_num', 'more_same_link', 'relative_news', 'user_name', 'datetime', 'summary', 'source_website', 'category']
    RESP_ITER_KEYS_WEIXIN_PUBLIC = ['key', 'tplid', 'classid', 'id', 'title', 'title1', 'date', 'thumbnail_url', 'user_image_url', 'user_name', 'content168', 'isV', 'user_id', 'summary', 'showurl', 'url', 'pagesize', 'timestamp', 'source_website', 'category']
    RESP_ITER_KEYS_WEIXIN_SEARCH = ['id', 'thumbnail_url', 'title', 'url', 'summary', 'user_url', 'user_name', 'timestamp', 'date', 'source_website', 'category']
    RESP_ITER_KEYS_TIANYA_BBS = ['id', 'title', 'url', 'summary', 'source_from_url', 'source_from_name', 'user_url', 'user_name', 'timestamp', 'datetime', 'replies', 'source_website', 'category']
    RESP_ITER_KEYS_XINHUA_BBS = ['id', 'title', 'url', 'summary', 'user_url', 'user_name', 'timestamp', 'datetime','source_website', 'category']
    
    def __init__(self):
        super(ScrapyBoatItem, self).__init__()
        default_none_keys = []
        default_none_keys.extend(self.RESP_ITER_KEYS_BAIDU)
        default_none_keys.extend(self.RESP_ITER_KEYS_WEIXIN_PUBLIC)
        default_none_keys.extend(self.RESP_ITER_KEYS_WEIXIN_SEARCH)
        default_none_keys.extend(self.RESP_ITER_KEYS_TIANYA_BBS)
        default_none_keys.extend(self.RESP_ITER_KEYS_XINHUA_BBS)

        for key in default_none_keys:
            self.setdefault(key, None)

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (ScrapyBoatItem)):
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

