# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class ScrapyBoatItem(Item):
    # define the fields for your item here like:
    id = Field()
    title = Field() # 原文标题,【新闻速递】亚洲造船专家齐聚韩国济州岛  \u2014\u2014第八届亚...
    url = Field() # 原文链接
    summary = Field() # 文本概述
    timestamp = Field() # 时间戳，自1970-1-1的秒数
    datetime = Field() # 2011-02-21 17:35:47
    date = Field() # 2014-11-28
    thumbnail_url = Field() # 缩略图url
    user_id = Field() # 用户id
    user_url = Field() # 用户url
    user_image_url = Field() # 用户头像url, 公众平台帐号头像url, http://wx.qlogo.cn/mmhead/Q3auHgzwzM4Ot2SWhTdlicTICNicOH9fgDAicuX16sYicPCZDle7aicxvcQ/0
    user_name = Field() # 用户名, 公众帐号名, 中船重工经济研究中心
    source_website = Field() # 来源渠道
    category = Field() # 信息类别
    replies = Field()
    clicks = Field()
    website_name = Field()
    website_url = Field()
    # baidu
    same_news_num = Field() # 相同新闻数
    more_same_link = Field() # 相同新闻链接
    relative_news = Field() # 关联的新闻

    # weixin public
    key = Field() # http://mp.weixin.qq.com/
    tplid = Field() # 550
    classid = Field() # 11002601
    # docid = Field() # document id ,用id字段替换, ab735a258a90e8e1-6bee54fcbd896b2a-964b1fa79f51be4294b2819a08235c0a
    title1 = Field() # 【新闻速递】亚洲造船专家齐聚韩国济州岛  \u2014\u2014第八届亚洲造船专家技术论坛(ASEF)
    content168 = Field()
    isV = Field() # 1
    # openid = Field() # 公众帐号id, 用user_id替换, oIWsFt8kxiyiYRj6oWsCQL3hHsqU
    # content = Field() # 用summary代替, 点击上方\u201c蓝色字体\u201d可以订阅哦!亚洲造船专家齐聚韩国济州岛\u2014\u2014第八届亚洲造船专家技术论坛(ASEF) 2014年11月27日-28日...
    showurl = Field() # 微信 - mp.weixin.qq.com
    pagesize = Field() # 31k
    # lastModified = Field() # 最后修改时间戳，用timestamp的替换

    # weixin search
    # post_id = Field() # document id ,用id字段替换, ab735a258a90e8e1-6bee54fcbd896b2a-7fa89f251bc5802b223ed97b15bb48d4

    #tianya bbs
    source_from_url = Field() # 帖子来源版块url
    source_from_name = Field() # 帖子来源版块名称
    replies = Field() # 回复数

    RESP_ITER_KEYS_BAIDU = ['id', 'title', 'url', 'same_news_num', 'more_same_link', 'relative_news', 'user_name', 'timestamp', 'datetime', 'date', 'summary', 'source_website', 'category']
    RESP_ITER_KEYS_WEIXIN_PUBLIC = ['key', 'tplid', 'classid', 'id', 'title', 'title1', 'date', 'datetime', 'thumbnail_url', 'user_image_url', 'user_name', 'content168', 'isV', 'user_id', 'summary', 'showurl', 'url', 'pagesize', 'timestamp', 'source_website', 'category']
    RESP_ITER_KEYS_WEIXIN_SEARCH = ['id', 'thumbnail_url', 'title', 'url', 'summary', 'user_url', 'user_name', 'timestamp', 'date', 'datetime', 'source_website', 'category']
    RESP_ITER_KEYS_TIANYA_BBS = ['id', 'title', 'url', 'summary', 'source_from_url', 'source_from_name', 'user_url', 'user_name', 'timestamp', 'date', 'datetime', 'replies', 'source_website', 'category']
    RESP_ITER_KEYS_XINHUA_BBS = ['id', 'title', 'url', 'summary', 'user_url', 'user_name', 'timestamp', 'date', 'datetime','source_website', 'category']
    
    def __init__(self):
        super(ScrapyBoatItem, self).__init__()
        default_none_keys = []
        default_none_keys.extend(self.RESP_ITER_KEYS_BAIDU)
        default_none_keys.extend(self.RESP_ITER_KEYS_WEIXIN_PUBLIC)
        default_none_keys.extend(self.RESP_ITER_KEYS_WEIXIN_SEARCH)
        default_none_keys.extend(self.RESP_ITER_KEYS_TIANYA_BBS)
        default_none_keys.extend(self.RESP_ITER_KEYS_XINHUA_BBS)

        for key in default_none_keys:
            default = self.setdefault(key, None)
        # print default

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (ScrapyBoatItem)):
                d[k] = v.to_dict()
            else:
                d[k] = v

        return d

class ScrapyRenwuItem(Item):
    id = Field()
    url = Field()
    thumbnail_url = Field()
    title = Field()
    summary = Field()
    clicks = Field()
    replies = Field()
    website_name = Field()
    website_url = Field()
    user_name = Field()
    user_url = Field()
    datetime = Field()
    timestamp = Field()
    date = Field()
    tag = Field()
    source_website = Field()
    RESP_ITER_KEYS_CHUANREN_NEWS = ['id', 'url', 'thumbnail_url', 'title', 'summary', 'clicks', 'replies', 'website_name', 'website_url', 'user_name', 'user_url', 'datetime', 'timestamp', 'date', 'source_website']
    RESP_ITER_KEYS_HAISHI_NEWS = ['id', 'url', 'thumbnail_url', 'title', 'summary', 'replies', 'tag', 'datetime', 'timestamp', 'date', 'source_website']
    RESP_ITER_KEYS_GUOCHUAN_NEWS = ['id', 'title', 'url', 'thumbnail_url', 'summary', 'timestamp', 'date', 'datetime', 'source_website']

    def __init__(self):
        super(ScrapyRenwuItem, self).__init__()
        default_keys = []
        default_keys.extend(self.RESP_ITER_KEYS_HAISHI_NEWS)
        default_keys.extend(self.RESP_ITER_KEYS_GUOCHUAN_NEWS)

        for key in default_keys:
            value = self.setdefault(key, None)

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (ScrapyRenwuItem)):
                d[k] = v.to_dict()
            else:
                d[k] = v

        return d

class ChuanrenItem(Item):
    id = Field()
    url = Field()
    thumbnail_url = Field()
    title = Field()
    summary = Field()
    clicks = Field()
    replies = Field()
    website_name = Field()
    website_url = Field()
    user_name = Field()
    user_url = Field()
    datetime = Field()
    timestamp = Field()
    date = Field()
    source_website = Field()


    RESP_ITER_KEYS_CHUANREN_NEWS = ['id', 'url', 'thumbnail_url', 'title', 'summary', 'clicks', 'replies', 'website_name', 'website_url', 'user_name', 'user_url', 'datetime', 'timestamp', 'date', 'source_website']

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (ChuanrenItem)):
                d[k] = v.to_dict()
            else:
                d[k] = v

        return d

class HaishiItem(Item):
    id = Field()
    url = Field()
    thumbnail_url = Field()
    title = Field()
    summary = Field()
    replies = Field()
    tag = Field()
    datetime = Field()
    timestamp = Field()
    date = Field()
    source_website = Field()


    RESP_ITER_KEYS_HAISHI_NEWS = ['id', 'url', 'thumbnail_url', 'title', 'summary', 'replies', 'tag', 'datetime', 'timestamp', 'date', 'source_website']
    
    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (HaishiItem)):
                d[k] = v.to_dict()
            else:
                d[k] = v

        return d

class GuochuanItem(Item):
    id = Field()
    title = Field()
    url = Field()
    thumbnail_url = Field()
    summary = Field()
    timestamp = Field()
    date = Field()
    datetime = Field()
    source_website = Field()


    RESP_ITER_KEYS_GUOCHUAN_NEWS = ['id', 'title', 'url', 'thumbnail_url', 'summary', 'timestamp', 'date', 'datetime', 'source_website']

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (GuochuanItem)):
                d[k] = v.to_dict()
            else:
                d[k] = v

        return d     


class ZhengyiItem(Item):
    id = Field()
    title = Field()
    url = Field()
    summary = Field()
    timestamp = Field()
    date = Field()
    datetime = Field()
    source_website = Field()
    category = Field()


    RESP_ITER_KEYS_ZHENGYI = ['id', 'title', 'url', 'summary', 'timestamp', 'date', 'datetime', 'source_website', 'category']

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (ZhengyiItem)):
                d[k] = v.to_dict()
            else:
                d[k] = v

        return d        


class UserItem(Item):
    """
    search spider，字段值中有转义符
    """
    id = Field() # 用户UID, 2854532022,
    # idstr = Field() # 字符串型用户ID, 与id字段重复, 不用存, "2854532022"
    class_type = Field() # 1, ?
    screen_name = Field() # "Come_On_TAO", 用户昵称
    name = Field() # "Come_On_Tao", 友好显示名称
    province = Field() # "100", 用户所在省级ID
    city = Field() # "1000", 用户所在城市ID
    location = Field() # "\u5176\u4ed6", 用户所在地
    description = Field() # 用户自我描述
    url = Field() # 用户博客地址
    profile_image_url = Field() # 用户头像地址（中图），50×50像素
    profile_url = Field() # 用户的微博统一URL地址, http://weibo.com/profile_url就是用户微博主页
    domain = Field() # 用户个性化URL, 同上
    weihao = Field() # 用户的微号(新浪微博用户个性化纯数字号码), ""
    gender = Field() # 用户性别, 'f'
    followers_count = Field() # 粉丝数
    friends_count = Field() # 关注数
    pagefriends_count = Field() # ?
    statuses_count = Field() # 微博数
    favourites_count = Field() # 收藏数
    created_at = Field() # 注册日期, "Thu Jun 28 21:13:09 +0800 2012"
    timestamp = Field() # created_at字段转化而来的时间戳
    following = Field() # false, ?
    allow_all_act_msg = Field() # true, 是否允许所有人给我发私信，true：是，false：否
    geo_enabled = Field() # 是否允许标识用户的地理位置, false
    verified = Field() # 加V标示，是否微博认证用户, false
    verified_type = Field() # 用户认证类型, -1
    ptype = Field() # 0
    allow_all_comment = Field() # 是否允许所有人对我的微博进行评论
    avatar_large = Field() # 用户头像地址（大图），180×180像素
    avatar_hd = Field() # 用户头像地址（高清），高清头像原图
    verified_reason = Field() # 认证原因, ""
    verified_trade = Field() # "", ?
    verified_reason_url = Field() # "", ?
    verified_source = Field() # "", ?
    verified_source_url = Field() # "", ?
    follow_me = Field() # false, 该用户是否关注当前登录用户，true：是，false：否
    online_status = Field() # 用户的在线状态，0：不在线、1：在线
    bi_followers_count = Field() # 用户的互粉数
    lang = Field() # 用户当前的语言版本，"zh-cn"：简体中文，"zh-tw"：繁体中文，"en"：英语
    star = Field() # 0, ?
    mbtype = Field() # 12, ?
    mbrank = Field() # 5, ?
    block_word = Field() # 1, ?
    block_app = Field() # 1, ?
    credit_score = Field() # ?

    cover_image = Field() # 用户封面地址
    cover_image_phone = Field() # ?
    ulevel = Field() # 0, ?
    badge_top = Field() # "", ?
    extend = Field() # ?, {"privacy":{"mobile":0},"mbprivilege":"0000000000000000000000000000000000000000000000000000000000000000"}
    remark = Field() # "" ?
    verified_state = Field() # 0
    # uids list
    followers = Field() # just uids
    friends = Field() # just uids
    # 自定义字段
    first_in = Field()
    last_modify = Field()
    
    # utils.py中解析返回数据的字段
    RESP_ITER_KEYS = ['id', 'name', 'class_type', 'gender', 'province', 'city', 'location', 'url', 'domain', \
    'geo_enabled', 'verified', 'verified_type', 'description', \
    'followers_count', 'statuses_count', 'friends_count', 'favourites_count', \
    'profile_image_url', 'allow_all_act_msg', 'created_at']
    
    # mongodb pipelines中更新的字段
    PIPED_UPDATE_KEYS = ['name', 'class_type', 'gender', 'province', 'city', 'location', 'url', 'domain', \
    'geo_enabled', 'verified', 'verified_type', 'description', \
    'followers_count', 'statuses_count', 'friends_count', 'favourites_count', \
    'profile_image_url', 'allow_all_act_msg', 'created_at']

    def __init__(self):
        """
        >>> a = UserItem()
        >>> a
        {'followers': [], 'friends': []}
        >>> a.to_dict()
        {'followers': [], 'friends': []}
        """
        super(UserItem, self).__init__()

        default_empty_arr_keys = ['followers', 'friends']
        for key in default_empty_arr_keys:
            self.setdefault(key, [])

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (UserItem, WeiboItem)):
                d[k] = v.to_dict()
            else:
                d[k] = v
        return d

class WeiboItem(Item):
    """
    search spider，字段值中有转义符
    """
    id = Field() # 16位微博ID, 3752470516005693
    uid = Field() # just uid, 用户uid
    user = Field() # user info dict
    mid = Field() # 16位微博ID, "3752470516005693"
    created_at = Field() # 微博创建时间, "Mon Sep 08 10:09:10 +0800 2014"
    timestamp = Field() # created_at字段转化而来的时间戳
    text = Field() # unicode, 微博信息内容
    source = Field() # 微博来源, <a href=\"http:\/\/app.weibo.com\/t\/feed\/8crQy\" rel=\"nofollow\">Weico.iPhone<\/a>",

    favorited = Field() # false, 是否已收藏，true：是，false：否
    truncated = Field() # false, 是否被截断，true：是，false：否
    in_reply_to_status_id = Field() # "", 回复ID
    in_reply_to_user_id = Field() # "", 回复人UID
    in_reply_to_screen_name = Field() # "", 回复人昵称
    geo = Field() # null, 地理信息字段
    reposts_count = Field() # 转发数
    comments_count = Field() # 评论数
    attitudes_count = Field() # 赞数
    mlevel = Field() # 0, ?
    visible = Field() # 微博的可见性及指定可见分组信息, 该object中type取值，0：普通微博，1：私密微博，3：指定分组微博，4：密友微博; list_id为分组的组号
    
    pic_ids = Field() # queryWeiboBykw返回该字段, 微博配图id, 多图时返回多图id, 无配图返回“[]”, 转发微博无法配图此字段为[]
    pic_urls = Field() # queryUserWeibo返回该字段, [{"thumbnail_pic": "http://ww4.sinaimg.cn/thumbnail/475b3d56gw1ek4vgg9x3xj20c60ee0t7.jpg"},]
    
    pid = Field() # 3752469458416290, ?, 原创微博无该字段
    thumbnail_pic = Field() # 缩略图片地址，没有时不返回此字段, 转发微博无法配图不返回该字段
    bmiddle_pic = Field() # 中等尺寸图片地址，没有时不返回此字段, 转发微博无法配图不返回该字段
    original_pic = Field() # 原始图片地址，没有时不返回此字段, 转发微博无法配图不返回该字段
    retweeted_status = Field() # 源微博dict
    annotations = Field() # ?, 转发微博无该字段，原创微博有该字段, [{"client_mblogid":"iPhone-2849F7C0-695E-4C50-B9A9-101770EEFC70"}]
    reposts = Field() # just mids, 转发微博id列表
    comments = Field() # just ids, 评论微博id列表
    category = Field() # 31, ?, 转发微博有该字段，原创微博无该字段

    floor_num = Field() # 楼号 3
    reply_comment = Field() # 回复的评论mid

    # ad = Field() # 微博流内的推广微博ID, 没有该字段
    # url_objects = Field() # 有该字段，但太长没有必要，?
    # idstr = Field() # 16位微博ID, 和mid重复不用存, 字符串型微博ID, "3752470516005693"
    # darwin_tags = Field() # [], ?

    # 自定义字段
    first_in = Field()
    last_modify = Field()
    source_website = Field() # 来源
    source_category = Field() # 类别

    RESP_ITER_KEYS = ['created_at', 'id', 'mid', 'text', 'source', 'favorited', 'truncated', \
            'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name', \
            'pic_urls', 'thumbnail_pic', 'geo', 'reposts_count', 'comments_count', \
            'attitudes_count', 'source_website', 'source_category']

    PIPED_UPDATE_KEYS = ['created_at', 'source', 'favorited', 'truncated', \
    'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name', \
    'pic_urls', 'thumbnail_pic', 'geo', 'reposts_count', 'comments_count', \
    'attitudes_count', 'source_website', 'source_category']

    def __init__(self):
        super(WeiboItem, self).__init__()
        default_empty_arr_keys = ['reposts', 'comments']
        for key in default_empty_arr_keys:
            self.setdefault(key, [])

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (UserItem, WeiboItem)):
                d[k] = v.to_dict()
            else:
                d[k] = v
        return d

