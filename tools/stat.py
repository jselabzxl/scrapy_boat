#-*-coding=utf-8-*-

import os
import csv
import time
import collections
from xapian_case.utils import load_scws, cut
from utils import START_DATETIME, END_DATETIME, _default_mongo, get_module_keywords, START_TS, END_TS

result_path = "./%s-%s/" % (START_DATETIME, END_DATETIME)
if not os.path.exists(result_path):
    os.mkdir(result_path)

s = load_scws()

mongo = _default_mongo()

query_dict = {
    "timestamp": {
        "$gte": START_TS,
        "$lt": END_TS
    },
    "keywords_hit": True,
    "rubbish": False
}

def ts2date(ts):
    return time.strftime('%Y-%m-%d', time.localtime(ts))

def _encode_utf8(us):
    if isinstance(us, unicode):
        us = us.encode('utf-8')

    if not us:
        us = ''

    return us

def get_keywords(keywords_file):
    keywords = []
    keywords_file = '../source/' + keywords_file
    f = open(keywords_file)
    for line in f:
        if '!' in line:
            strip_no_querys = []
            querys = line.strip().lstrip('(').rstrip(')').split(' | ')
            for q in querys:
                strip_no_querys.append(q.split(' !')[0])
            strip_no_querys = '+'.join(strip_no_querys)
            line = strip_no_querys
        keywords_para = line.strip().lstrip('(').rstrip(')').split(' | ')
        keywords.extend(keywords_para)
    f.close()

    return keywords


def sheqi_stat():
    texts = []
    keywords = get_keywords('keywords_corp_baidu.txt')

    # 发布来源统计
    author_dict = dict()

    # 涉及企业的信息数统计
    corp_dict = dict()

    # 各渠道信息条数的周走势
    source_daily_dict = {
        "微博": {},
        "微信": {},
        "论坛": {},
        "新闻": {}
    }

    # 微博论坛渠道的情绪统计
    sentiment_dict = dict()

    # 统计关键词
    total_keywords_list = []

    query_dict["$or"] = [{"source_category": "keywords_corp_weiboapi.txt"}, {"source_category": "keywords_hot_weiboapi.txt"}, {"source_category": "keywords_leader_weiboapi.txt"}]
    query_dict["source_website"] = "weibo_api_search_spider"
    count = mongo.master_timeline_weibo.find(query_dict).count()
    results = mongo.master_timeline_weibo.find(query_dict)
    author_dict["微博"] = count
    for r in results:
        texts.append(r['text'].encode('utf-8'))
        try:
            source_daily_dict["微博"][ts2date(r["timestamp"])] += 1
        except KeyError:
            source_daily_dict["微博"][ts2date(r["timestamp"])] = 1

        try:
            sentiment_dict[r["sentiment"]] += 1
        except KeyError:
            sentiment_dict[r["sentiment"]] = 1

    query_dict["$or"] = [{"category": "keywords_corp_forum.txt"}, {"category": "keywords_hot_forum.txt"}, {"category": "keywords_leader_forum.txt"}]
    del query_dict["source_website"]
    count = mongo.boatcol.find(query_dict).count()
    results = mongo.boatcol.find(query_dict)
    author_dict["论坛"] = count
    for r in results:
        title = _encode_utf8(r['title'])
        content168 = _encode_utf8(r['content168'])
        summary = _encode_utf8(r['summary'])

        text = title  + content168 + summary
        texts.append(text)
        try:
            source_daily_dict["论坛"][r["date"]] += 1
        except KeyError:
            source_daily_dict["论坛"][r["date"]] = 1

        try:
            sentiment_dict[r["sentiment"]] += 1
        except KeyError:
            sentiment_dict[r["sentiment"]] = 1

    query_dict["$or"] = [{"category": "keywords_corp_weixin.txt"}, {"category": "keywords_hot_weixin.txt"}, {"category": "keywords_leader_weixin.txt"}]
    count = mongo.boatcol.find(query_dict).count()
    results = mongo.boatcol.find(query_dict)
    author_dict["微信"] = count
    for r in results:
        title = _encode_utf8(r['title'])
        content168 = _encode_utf8(r['content168'])
        summary = _encode_utf8(r['summary'])

        text = title  + content168 + summary
        texts.append(text)
        try:
            source_daily_dict["微信"][r["date"]] += 1
        except KeyError:
            source_daily_dict["微信"][r["date"]] = 1

    query_dict["$or"] = [{"category": "keywords_corp_baidu.txt"}, {"category": "keywords_hot_baidu.txt"}, {"category": "keywords_leader_baidu.txt"}]
    query_dict["source_website"] = "baidu_ns_search"
    results = mongo.boatcol.find(query_dict)
    for r in results:
        try:
            author_dict[r['user_name']] += 1
        except KeyError:
            author_dict[r['user_name']] = 1
        title = _encode_utf8(r['title'])
        content168 = _encode_utf8(r['content168'])
        summary = _encode_utf8(r['summary'])

        text = title  + content168 + summary
        texts.append(text)
        try:
            source_daily_dict["新闻"][r["date"]] += 1
        except KeyError:
            source_daily_dict["新闻"][r["date"]] = 1

    fw = csv.writer(open(result_path + 'sheqi_author_stat_%s_%s.csv' % (START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    results = sorted(author_dict.iteritems(), key=lambda(k, v): v, reverse=True)
    for k, v in results:
        if k == "":
            continue
        fw.writerow((_encode_utf8(k), v))

    for text in texts:
        cut_kw = cut(s, text)
        total_keywords_list.extend(cut_kw)
        for keyword in keywords:
            if keyword in text:
                try:
                    corp_dict[keyword] += 1
                except KeyError:
                    corp_dict[keyword] = 1

    fw = csv.writer(open(result_path + 'sheqi_gongsi_stat_%s_%s.csv' % (START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    results = sorted(corp_dict.iteritems(), key=lambda(k, v): v, reverse=True)
    for k, v in results:
        if k == "":
            continue
        fw.writerow((_encode_utf8(k), v))

    fw = csv.writer(open(result_path + 'sheqi_source_stat_%s_%s.csv' % (START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    for source, daily_dict in source_daily_dict.iteritems():
        for date, count in daily_dict.iteritems():
            fw.writerow((_encode_utf8(source), date, count))

    fw = csv.writer(open(result_path + 'sheqi_sentiment_stat_%s_%s.csv' % (START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    for sentiment, count in sentiment_dict.iteritems():
        fw.writerow((sentiment, count))

    ct = collections.Counter(total_keywords_list)
    keywords_results = ct.most_common(50)
    fw = csv.writer(open(result_path + 'sheqi_keywords_stat_%s_%s.csv' % (START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    for keyword, count in keywords_results:
        fw.writerow((_encode_utf8(keyword), count))

def enemy_stat():
    texts = []
    keywords = get_keywords('keywords_enemy_baidu.txt')

    # 涉及企业的與情热度统计
    corp_dict = dict()

    # 统计关键词
    total_keywords_list = []

    query_dict["$or"] = [{"source_category": "keywords_enemy_weiboapi.txt"}]
    query_dict["source_website"] = "weibo_api_search_spider"
    count = mongo.master_timeline_weibo.find(query_dict).count()
    results = mongo.master_timeline_weibo.find(query_dict)
    for r in results:
        if 'hot' in r:
            hot = r['hot']
        else:
            hot = 1
        texts.append([r['text'].encode('utf-8'), hot])

    query_dict["$or"] = [{"category": "keywords_enemy_forum.txt"}]
    del query_dict["source_website"]
    count = mongo.boatcol.find(query_dict).count()
    results = mongo.boatcol.find(query_dict)
    for r in results:
        title = _encode_utf8(r['title'])
        content168 = _encode_utf8(r['content168'])
        summary = _encode_utf8(r['summary'])

        text = title  + content168 + summary
        if 'hot' in r:
            hot = r['hot']
        else:
            hot = 1
        texts.append([text, hot])

    query_dict["$or"] = [{"category": "keywords_enemy_weixin.txt"}]
    count = mongo.boatcol.find(query_dict).count()
    results = mongo.boatcol.find(query_dict)
    for r in results:
        title = _encode_utf8(r['title'])
        content168 = _encode_utf8(r['content168'])
        summary = _encode_utf8(r['summary'])

        text = title  + content168 + summary
        if 'hot' in r:
            hot = r['hot']
        else:
            hot = 1
        texts.append([text, hot])

    query_dict["$or"] = [{"category": "keywords_enemy_baidu.txt"}]
    query_dict["source_website"] = "baidu_ns_search"
    results = mongo.boatcol.find(query_dict)
    for r in results:
        title = _encode_utf8(r['title'])
        content168 = _encode_utf8(r['content168'])
        summary = _encode_utf8(r['summary'])

        text = title  + content168 + summary
        if 'hot' in r:
            hot = r['hot']
        else:
            hot = 1
        texts.append([text, hot])

    for text in texts:
        cut_kw = cut(s, text[0])
        total_keywords_list.extend(cut_kw)
        for keyword in keywords:
            if keyword in text[0]:
                if text[1] == 0:
                    hot = 1
                else:
                    hot = text[1]
                try:
                    corp_dict[keyword] += hot
                except KeyError:
                    corp_dict[keyword] = hot

    fw = csv.writer(open(result_path + 'enemy_gongsi_stat_%s_%s.csv' % (START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    results = sorted(corp_dict.iteritems(), key=lambda(k, v): v, reverse=True)
    for k, v in results:
        if k == "":
            continue
        fw.writerow((_encode_utf8(k), v))

    ct = collections.Counter(total_keywords_list)
    keywords_results = ct.most_common(50)
    fw = csv.writer(open(result_path + 'enemy_keywords_stat_%s_%s.csv' % (START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    for keyword, count in keywords_results:
        fw.writerow((_encode_utf8(keyword), count))

def friends_stat():
    texts = []
    keywords = get_keywords('keywords_friends_baidu.txt')

    # 涉及企业的與情热度统计
    corp_dict = dict()

    # 统计关键词
    total_keywords_list = []

    query_dict["$or"] = [{"source_category": "keywords_friends_weiboapi.txt"}]
    query_dict["source_website"] = "weibo_api_search_spider"
    count = mongo.master_timeline_weibo.find(query_dict).count()
    results = mongo.master_timeline_weibo.find(query_dict)
    for r in results:
        if 'hot' in r:
            hot = r['hot']
        else:
            hot = 1
        texts.append([r['text'].encode('utf-8'), hot])

    query_dict["$or"] = [{"category": "keywords_friends_forum.txt"}]
    del query_dict["source_website"]
    count = mongo.boatcol.find(query_dict).count()
    results = mongo.boatcol.find(query_dict)
    for r in results:
        title = _encode_utf8(r['title'])
        content168 = _encode_utf8(r['content168'])
        summary = _encode_utf8(r['summary'])

        text = title  + content168 + summary
        if 'hot' in r:
            hot = r['hot']
        else:
            hot = 1
        texts.append([text, hot])

    query_dict["$or"] = [{"category": "keywords_friends_weixin.txt"}]
    count = mongo.boatcol.find(query_dict).count()
    results = mongo.boatcol.find(query_dict)
    for r in results:
        title = _encode_utf8(r['title'])
        content168 = _encode_utf8(r['content168'])
        summary = _encode_utf8(r['summary'])

        text = title  + content168 + summary
        if 'hot' in r:
            hot = r['hot']
        else:
            hot = 1
        texts.append([text, hot])

    query_dict["$or"] = [{"category": "keywords_friends_baidu.txt"}]
    query_dict["source_website"] = "baidu_ns_search"
    results = mongo.boatcol.find(query_dict)
    for r in results:
        title = _encode_utf8(r['title'])
        content168 = _encode_utf8(r['content168'])
        summary = _encode_utf8(r['summary'])

        text = title  + content168 + summary
        if 'hot' in r:
            hot = r['hot']
        else:
            hot = 1
        texts.append([text, hot])

    for text in texts:
        cut_kw = cut(s, text[0])
        total_keywords_list.extend(cut_kw)
        for keyword in keywords:
            if keyword in text[0]:
                if text[1] == 0:
                    hot = 1
                else:
                    hot = text[1]
                try:
                    corp_dict[keyword] += hot
                except KeyError:
                    corp_dict[keyword] = hot

    fw = csv.writer(open(result_path + 'friends_gongsi_stat_%s_%s.csv' % (START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    results = sorted(corp_dict.iteritems(), key=lambda(k, v): v, reverse=True)
    for k, v in results:
        if k == "":
            continue
        fw.writerow((_encode_utf8(k), v))

    ct = collections.Counter(total_keywords_list)
    keywords_results = ct.most_common(50)
    fw = csv.writer(open(result_path + 'friends_keywords_stat_%s_%s.csv' % (START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    for keyword, count in keywords_results:
        fw.writerow((_encode_utf8(keyword), count))


def domain_stat():
    texts = []
    keywords = get_keywords('keywords_domain_baidu.txt')

    # 统计关键词
    total_keywords_list = []

    query_dict["$or"] = [{"source_category": "keywords_domain_weiboapi.txt"}]
    query_dict["source_website"] = "weibo_api_search_spider"
    count = mongo.master_timeline_weibo.find(query_dict).count()
    results = mongo.master_timeline_weibo.find(query_dict)
    for r in results:
        texts.append(r['text'].encode('utf-8'))

    query_dict["$or"] = [{"category": "keywords_domain_forum.txt"}]
    del query_dict["source_website"]
    count = mongo.boatcol.find(query_dict).count()
    results = mongo.boatcol.find(query_dict)
    for r in results:
        title = _encode_utf8(r['title'])
        content168 = _encode_utf8(r['content168'])
        summary = _encode_utf8(r['summary'])

        text = title  + content168 + summary
        texts.append(text)

    query_dict["$or"] = [{"category": "keywords_domain_weixin.txt"}]
    count = mongo.boatcol.find(query_dict).count()
    results = mongo.boatcol.find(query_dict)
    for r in results:
        title = _encode_utf8(r['title'])
        content168 = _encode_utf8(r['content168'])
        summary = _encode_utf8(r['summary'])

        text = title  + content168 + summary
        texts.append(text)

    query_dict["$or"] = [{"category": "keywords_domain_baidu.txt"}]
    query_dict["source_website"] = "baidu_ns_search"
    results = mongo.boatcol.find(query_dict)
    for r in results:
        title = _encode_utf8(r['title'])
        content168 = _encode_utf8(r['content168'])
        summary = _encode_utf8(r['summary'])

        text = title  + content168 + summary
        texts.append(text)

    for text in texts:
        cut_kw = cut(s, text)
        total_keywords_list.extend(cut_kw)

    ct = collections.Counter(total_keywords_list)
    keywords_results = ct.most_common(50)
    fw = csv.writer(open(result_path + 'domain_keywords_stat_%s_%s.csv' % (START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    for keyword, count in keywords_results:
        fw.writerow((_encode_utf8(keyword), count))

if __name__=="__main__":
    print "stat begins..."
    sheqi_stat()
    enemy_stat()
    friends_stat()
    domain_stat()
    print "stat ends..."

