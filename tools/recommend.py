#-*-coding=utf-8-*-

import os
import csv
import pymongo
from duplicate import duplicate
from utils import START_DATETIME, END_DATETIME, _default_mongo, get_module_keywords, START_TS, END_TS

result_path = "./%s-%s/" % (START_DATETIME, END_DATETIME)
if not os.path.exists(result_path):
    os.mkdir(result_path)

mongo = _default_mongo()

def _encode_utf8(us):
    if isinstance(us, unicode):
        us = us.encode('utf-8')

    if not us:
        us = ''

    if isinstance(us, str):
        us = us.replace('\n', '')

    return us

WEIBO_KEYS = ['id', 'text', 'timestamp', 'created_at', 'uid', 'source_website', 'source_category', 'reposts_count', 'comments_count', 'attitudes_count', 'hot', 'rel_score', 'sensi', 'sentiment']

NEWS_KEYS = ['id', 'title', 'url', 'summary', 'timestamp', 'datetime', 'user_name', 'source_website', 'category', 'content168', 'hot', 'rel_score', 'sensi', 'sentiment']

def sheqi_rec(sort_field='hot'):
    module_keywords = [("sogou_weixin_search", "keywords_corp_weixin.txt"), \
            ("sogou_weixin_search", "keywords_leader_weixin.txt"), \
            ("sogou_weixin_search", "keywords_hot_weixin.txt"), \
            ("tianya_bbs_search", "keywords_corp_forum.txt"), \
            ("tianya_bbs_search", "keywords_leader_forum.txt"), \
            ("tianya_bbs_search", "keywords_hot_forum.txt"), \
            ("xinhua_bbs_search", "keywords_corp_forum.txt"), \
            ("xinhua_bbs_search", "keywords_leader_forum.txt"), \
            ("xinhua_bbs_search", "keywords_hot_forum.txt"), \
            ("baidu_ns_search", "keywords_corp_baidu.txt"), \
            ("baidu_ns_search", "keywords_leader_baidu.txt"), \
            ("baidu_ns_search", "keywords_hot_baidu.txt")]

    keywords_file_list = list(set([v for k, v in module_keywords]))

    query_dict = {
        "timestamp": {
            "$gte": START_TS,
            "$lt": END_TS
        },
        "keywords_hit": True,
        "rubbish": False,
        "category": {"$in": keywords_file_list},
    }

    count = mongo.boatcol.find(query_dict).count()
    print "sheqi news candidate %s count: " % sort_field, count
    results = mongo.boatcol.find(query_dict).sort(sort_field, pymongo.DESCENDING)

    results = [r for r in results]

    for r in results:
        r['title'] = r['title'].encode('utf-8')
        r['content'] = r['summary'].encode('utf-8')

    results = duplicate(results)

    fw = csv.writer(open(result_path + 'sheqi_news_sort_%s_%s_%s.csv' % (sort_field, START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    fw.writerow(NEWS_KEYS)
    for r in results:
        csvrow = []
        if r['duplicate'] == False:
            for key in NEWS_KEYS:
                csvrow.append(_encode_utf8(r[key]))

            fw.writerow(csvrow)

    module_keywords = [("weibo_api_search_spider", "keywords_corp_weiboapi.txt"), \
            ("weibo_api_search_spider", "keywords_leader_weiboapi.txt"), \
            ("weibo_api_search_spider", "keywords_hot_weiboapi.txt")]

    keywords_file_list = list(set([v for k, v in module_keywords]))

    query_dict = {
        "timestamp": {
            "$gte": START_TS,
            "$lt": END_TS
        },
        "keywords_hit": True,
        "rubbish": False,
        "source_category": {"$in": keywords_file_list},
    }

    count = mongo.master_timeline_weibo.find(query_dict).count()
    print "sheqi weibo candidate %s count: " % sort_field, count
    results = mongo.master_timeline_weibo.find(query_dict).sort(sort_field, pymongo.DESCENDING)

    results = [r for r in results]

    for r in results:
        r['title'] = ''.encode('utf-8')
        r['content'] = r['text'].encode('utf-8')

    results = duplicate(results)

    fw = csv.writer(open(result_path + 'sheqi_weibo_sort_%s_%s_%s.csv' % (sort_field, START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    fw.writerow(WEIBO_KEYS)
    for r in results:
        csvrow = []
        if r['duplicate'] == False:
            for key in WEIBO_KEYS:
                csvrow.append(_encode_utf8(r[key]))

            fw.writerow(csvrow)


def domain_rec(sort_field='hot'):
    module_keywords = [("sogou_weixin_search", "keywords_domain_weixin.txt"), \
            ("tianya_bbs_search", "keywords_domain_forum.txt"), \
            ("xinhua_bbs_search", "keywords_domain_forum.txt"), \
            ("baidu_ns_search", "keywords_domain_baidu.txt")]

    keywords_file_list = list(set([v for k, v in module_keywords]))

    query_dict = {
        "timestamp": {
            "$gte": START_TS,
            "$lt": END_TS
        },
        "keywords_hit": True,
        "rubbish": False,
        "category": {"$in": keywords_file_list},
    }

    count = mongo.boatcol.find(query_dict).count()
    print "domain news candidate %s count: " % sort_field, count
    results = mongo.boatcol.find(query_dict).sort(sort_field, pymongo.DESCENDING)

    results = [r for r in results]

    for r in results:
        r['title'] = r['title'].encode('utf-8')
        r['content'] = r['summary'].encode('utf-8')

    results = duplicate(results)

    fw = csv.writer(open(result_path + 'domain_news_sort_%s_%s_%s.csv' % (sort_field, START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    fw.writerow(NEWS_KEYS)
    for r in results:
        csvrow = []
        if r['duplicate'] == False:
            for key in NEWS_KEYS:
                csvrow.append(_encode_utf8(r[key]))

            fw.writerow(csvrow)


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

def enemy_rec(sort_field='hot'):
    keywords = get_keywords('keywords_enemy_baidu.txt')
    module_keywords = [("sogou_weixin_search", "keywords_enemy_weixin.txt"), \
            ("tianya_bbs_search", "keywords_enemy_forum.txt"), \
            ("xinhua_bbs_search", "keywords_enemy_forum.txt"), \
            ("baidu_ns_search", "keywords_enemy_baidu.txt")]

    keywords_file_list = list(set([v for k, v in module_keywords]))

    query_dict = {
        "timestamp": {
            "$gte": START_TS,
            "$lt": END_TS
        },
        "keywords_hit": True,
        "rubbish": False,
        "category": {"$in": keywords_file_list},
    }

    count = mongo.boatcol.find(query_dict).count()
    print "enemy news candidate %s count: " % sort_field, count
    results = mongo.boatcol.find(query_dict).sort(sort_field, pymongo.DESCENDING)

    results = [r for r in results]

    for r in results:
        r['title'] = r['title'].encode('utf-8')
        r['content'] = r['summary'].encode('utf-8')

    results = duplicate(results)

    fw = csv.writer(open(result_path + 'enemy_news_sort_%s_%s_%s.csv' % (sort_field, START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
    fw.writerow(NEWS_KEYS)
    # 按对手组织文本
    corp_news_dict = dict()
    for r in results:
        csvrow = []
        if r['duplicate'] == False:
            for key in NEWS_KEYS:
                csvrow.append(_encode_utf8(r[key]))

            fw.writerow(csvrow)

            if sort_field == 'hot':
                text = r['title'] + r['summary'].encode('utf-8')
                for keyword in keywords:
                    if keyword in text:
                        try:
                            corp_news_dict[keyword].append(r)
                        except KeyError:
                            corp_news_dict[keyword] = [r]

    if corp_news_dict != {}:
        fw = csv.writer(open(result_path + 'enemy_news_gongsi_%s_%s.csv' % (START_DATETIME, END_DATETIME), 'wb'), delimiter='^')
        new_keys = ['gongsi']
        new_keys += NEWS_KEYS
        fw.writerow(new_keys)
        for corp, news_dict in corp_news_dict.iteritems():
            for r in news_dict:
                csvrow = [corp]
                for key in NEWS_KEYS:
                    csvrow.append(_encode_utf8(r[key]))

                fw.writerow((csvrow))


if __name__ == "__main__":
    print "recommend begins..."
    sheqi_rec(sort_field='hot')
    sheqi_rec(sort_field='rel_score')
    sheqi_rec(sort_field='sensi')
    domain_rec(sort_field='hot')
    domain_rec(sort_field='rel_score')
    domain_rec(sort_field='sensi')
    enemy_rec(sort_field='hot')
    enemy_rec(sort_field='rel_score')
    enemy_rec(sort_field='sensi')
    print "recommend ends..."
