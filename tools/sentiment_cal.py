#-*-coding=utf-8-*-
"""情感计算
"""

from xapian_case.utils import load_scws, cut
from triple_sentiment_classifier import triple_classifier
from utils import _default_mongo, get_module_keywords, START_TS, END_TS

s = load_scws()

def diamond_classifier(item):
    # 其他类
    sentiment = 0

    if '【' in item['text'].encode('utf-8') and '】' in item['text'].encode('utf-8'):
        # 简单规则判断新闻类
        sentiment = 4
    else:
        # 积极、愤怒、悲伤3类情感分类器
        sentiment = triple_classifier(item)

    return sentiment

mongo = _default_mongo()

module_keywords = get_module_keywords()

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
        results = mongo.master_timeline_weibo.find(query_dict)

        for r in results:
            sentiment = diamond_classifier(r)
            r['sentiment'] = sentiment
            mongo.master_timeline_weibo.update({"_id": r["_id"]}, {"$set": r})
    else:
        query_dict["category"] = keywords_file
        query_dict["source_website"] = source_en
        count = mongo.boatcol.find(query_dict).count()
        results = mongo.boatcol.find(query_dict)

        for r in results:
            title = _encode_utf8(r['title'])
            content168 = _encode_utf8(r['content168'])
            summary = _encode_utf8(r['summary'])

            text = title  + content168 + summary
            item['text'] = text
            sentiment = diamond_classifier(r)
            r['sentiment'] = sentiment
            mongo.boatcol.update({"_id": r["_id"]}, {"$set": r})

    print source_en, keywords_file, count
