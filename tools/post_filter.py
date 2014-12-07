#-*-coding=utf-8-*-
"""关键词精炼
"""

from utils import _default_mongo, get_module_keywords, START_TS, END_TS


def keywords_hit(text, hit_keywords):
    hit = False
    for ks in hit_keywords:
        should_hits_count = 0
        not_words = None
        for k in ks:
            if not k.startswith("!"):
                should_hits_count += 1
            else:
                not_words = k.strip("!")

        hits_count = 0
        for k in ks:
            if k in text and not k.startswith("!"):
                if not not_words:
                    hits_count += 1
                if not_words and not_words not in text:
                    hits_count += 1

        if hits_count == should_hits_count:
            hit= True
            break

    rubbish_words = ['个股', '趋势', '股票', '涨停']
    for rub in rubbish_words:
        if rub in text:
            hit = False
            break

    if '【' in text and '】' in text and '验证' not in text:
        hit = True

    if '中国船舶大学' in text:
        hit = False

    return hit

def _encode_utf8(us):
    if isinstance(us, unicode):
        us = us.encode('utf-8')

    if not us:
        us = ''

    return us

def get_keywords(file_name):
    f = open('../source/' + file_name)
    hit_keywords = []
    for line in f:
        ks = line.strip().strip('(').strip(')').split(' | ')
        ks_list = [word.split(' ') for word in ks]
        for k in ks_list:
            hit_keywords.append(k)

    f.close()

    return hit_keywords

print "post filter begins..."

mongo = _default_mongo()

module_keywords = get_module_keywords()

for bankuai, lanmu, source, source_en, keywords_file in module_keywords:
    query_dict = {
        "timestamp": {
            "$gte": START_TS,
            "$lt": END_TS
        }
    }

    hit_keywords = get_keywords(keywords_file)

    if source_en == "weibo_api_search_spider":
        query_dict["source_category"] = keywords_file
        query_dict["source_website"] = source_en
        count = mongo.master_timeline_weibo.find(query_dict).count()
        results = mongo.master_timeline_weibo.find(query_dict)
        hit_count = 0
        for r in results:
            hit = keywords_hit(_encode_utf8(r['text']), hit_keywords)
            if hit:
                r['keywords_hit'] = True
                hit_count += 1
            else:
                r['keywords_hit'] = False

            mongo.master_timeline_weibo.update({"_id": r["_id"]}, {"$set": r})
    else:
        query_dict["category"] = keywords_file
        query_dict["source_website"] = source_en
        count = mongo.boatcol.find(query_dict).count()
        results = mongo.boatcol.find(query_dict)

        hit_count = 0
        for r in results:
            title = _encode_utf8(r['title'])
            content168 = _encode_utf8(r['content168'])
            summary = _encode_utf8(r['summary'])

            text = title  + content168 + summary
            hit = keywords_hit(text, hit_keywords)
            if hit:
                r['keywords_hit'] = True
                hit_count += 1
            else:
                r['keywords_hit'] = False

            mongo.boatcol.update({"_id": r["_id"]}, {"$set": r})

    print source_en, keywords_file, count, hit_count

print "post filter ends..."
