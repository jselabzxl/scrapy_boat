#-*-coding=utf-8-*-
"""热度排序
"""

from utils import _default_mongo, get_module_keywords, START_TS, END_TS

print "hot_sort begins..."

media_weight = {}
f = open('media_weight_5.txt')
for line in f:
    media, times, weight =line.strip().split('\t')
    media = media.decode('utf-8')
    media_weight[media] = int(weight)
f.close()

def get_media_weight(media):
    w = 1
    if media in media_weight.keys():
        w = media_weight[media]

    return w

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
            hot = r['reposts_count']
            if hot == 0:
                hot = 1
            mongo.master_timeline_weibo.update({"_id": r["_id"]}, {"$set": {"hot": hot}})

    else:
        query_dict["category"] = keywords_file
        query_dict["source_website"] = source_en
        # query_dict["relative_news"] = None
        count = mongo.boatcol.find(query_dict).count()
        results = mongo.boatcol.find(query_dict)

        for r in results:
            if not r["relative_news"]:
                t_weight = 0
                relative_news = mongo.boatcol.find({"relative_news.id": r['id']})
                for rr in relative_news:
                    t_weight += get_media_weight(rr["user_name"])
            else:
                t_weight = get_media_weight(r["user_name"])
            if t_weight > 0:
                hot = t_weight
            else:
                hot = 1
            mongo.boatcol.update({"_id": r["_id"]}, {"$set": {"hot": hot}})

    print source_en, keywords_file, count

print "hot_sort ends..."
