#-*-coding=utf-8-*-

from xapian_case.utils import load_scws, cut
from utils import _default_mongo, get_module_keywords, START_TS, END_TS

def _encode_utf8(us):
    if isinstance(us, unicode):
        us = us.encode('utf-8')

    if not us:
        us = ''

    return us

print "cut word begins..."
s = load_scws()

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
            terms = cut(s, r['text'].encode('utf-8'))
            mongo.master_timeline_weibo.update({"_id": r["_id"]}, {"$set": {"terms": terms}})
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
            r['text'] = text.decode('utf-8')
            terms = cut(s, r['text'].encode('utf-8'))
            mongo.boatcol.update({"_id": r["_id"]}, {"$set": {"terms": terms}})

    print source_en, keywords_file, count

print 'cut word ends...'
