#-*-coding=utf-8-*-
"""词网相关度排序
"""

import sys
sys.path.append('./news/')
from test_rank import word_net, get_text_net
from utils import _default_mongo, get_module_keywords, START_TS, END_TS

def _encode_utf8(us):
    if isinstance(us, unicode):
        us = us.encode('utf-8')

    if not us:
        us = ''

    return us

print "rel_sort begins..."

mongo = _default_mongo()

module_keywords = get_module_keywords()

for bankuai, lanmu, source, source_en, keywords_file in module_keywords:
    query_dict = {
        "timestamp": {
            "$gte": START_TS,
            "$lt": END_TS
        },
        "keywords_hit": True,
        "rubbish": False,
    }

    if source_en == "weibo_api_search_spider":
        query_dict["source_category"] = keywords_file
        query_dict["source_website"] = source_en
        count = mongo.master_timeline_weibo.find(query_dict).count()
        results = mongo.master_timeline_weibo.find(query_dict)

        inputs = []
        for r in results:
            text = _encode_utf8(r['text'])
            r['text4wordnet'] = text
            inputs.append(r)
        
        flag = keywords_file
        wordnet_results = word_net(inputs)
        if len(wordnet_results):
            results = get_text_net(flag, inputs, wordnet_results)
            for weight, r in results:
                r['rel_score'] = weight
                mongo.master_timeline_weibo.update({"_id": r["_id"]}, {"$set": r})

    else:
        query_dict["category"] = keywords_file
        query_dict["source_website"] = source_en
        count = mongo.boatcol.find(query_dict).count()
        results = mongo.boatcol.find(query_dict)

        inputs = []
        for r in results:
            title = _encode_utf8(r['title'])
            content168 = _encode_utf8(r['content168'])
            summary = _encode_utf8(r['summary'])

            text = title  + content168 + summary
            r['text4wordnet'] = text
            inputs.append(r)
        
        flag = keywords_file
        wordnet_results = word_net(inputs)
        results = get_text_net(flag, inputs, wordnet_results)
        for weight, r in results:
            r['rel_score'] = weight
            mongo.boatcol.update({"_id": r["_id"]}, {"$set": r})

    print source_en, keywords_file, count

print "rel_sort ends..."
