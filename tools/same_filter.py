#-*-coding=utf-8-*-
"""信息去重
"""

import pymongo
import Levenshtein
from utils import _default_mongo, get_module_keywords, START_TS, END_TS

SAME_RATIO_THESHOLD = 0.8 

def max_same_rate(items, item):
    #计算item 和 items 的相似度
    ratio_list = [Levenshtein.ratio(i['text4same_filter'], item['text4same_filter']) for i in items]
    if len(ratio_list):
        return max(ratio_list)
    else:
    	return 0

def _encode_utf8(us):
    if isinstance(us, unicode):
        us = us.encode('utf-8')

    if not us:
        us = ''

    return us

print "same_filter begins..."

mongo = _default_mongo()

module_keywords = get_module_keywords()

for sort_field in ['rel_score', 'hot', 'sensi']:
    for bankuai, lanmu, source, source_en, keywords_file in module_keywords:
        query_dict = {
            "timestamp": {
                "$gte": START_TS,
                "$lt": END_TS
            },
            "keywords_hit": True,
            "rubbish": False
        }

        if source_en == "weibo_api_search_spider":
            query_dict["source_category"] = keywords_file
            query_dict["source_website"] = source_en
            count = mongo.master_timeline_weibo.find(query_dict).count()
            results = mongo.master_timeline_weibo.find(query_dict).sort(sort_field, pymongo.DESCENDING)

            no_sames = []
            for r in results:
                text = _encode_utf8(r['text'])
                r['text4same_filter'] = text
                
                ratio = max_same_rate(no_sames, r)
                if ratio < SAME_RATIO_THESHOLD:
                    no_sames.append(r)
                    r['same_rubbish_' + sort_field] = False
                else:
                    r['same_rubbish_' + sort_field] = True
                
                mongo.master_timeline_weibo.update({"_id": r["_id"]}, {"$set": r})

        else:
            query_dict["category"] = keywords_file
            query_dict["source_website"] = source_en
            count = mongo.boatcol.find(query_dict).count()
            results = mongo.boatcol.find(query_dict).sort(sort_field, pymongo.DESCENDING)

            no_sames = []
            for r in results:
                title = _encode_utf8(r['title'])
                content168 = _encode_utf8(r['content168'])
                summary = _encode_utf8(r['summary'])

                text = title  + content168 + summary
                r['text4same_filter'] = text
                
                ratio = max_same_rate(no_sames, r)
                if ratio < SAME_RATIO_THESHOLD:
                    no_sames.append(r)
                    r['same_rubbish' + sort_field] = False
                else:
                    r['same_rubbish' + sort_field] = True
                
                mongo.boatcol.update({"_id": r["_id"]}, {"$set": r})

        print source_en, keywords_file, count, len(no_sames)

print "same_filter ends..."
