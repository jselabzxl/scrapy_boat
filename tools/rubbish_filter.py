#-*-coding=utf-8-*-
"""垃圾过滤
"""

from utils import _default_mongo, get_module_keywords, START_TS, END_TS


def rel_classifier(inputs):
    import sys
    sys.path.append('./libsvm-3.17/python/')
    from final import test, choose_ad

    flag = '1'
    test(inputs, flag)
    label = choose_ad(flag)

    return label

def _encode_utf8(us):
    if isinstance(us, unicode):
        us = us.encode('utf-8')

    if not us:
        us = ''

    return us

print "rubbish filter begins..."

mongo = _default_mongo()

module_keywords = get_module_keywords()

for bankuai, lanmu, source, source_en, keywords_file in module_keywords:
    query_dict = {
        "timestamp": {
            "$gte": START_TS,
            "$lt": END_TS
        },
        "keywords_hit": True
    }

    if source_en == "weibo_api_search_spider":
        query_dict["source_category"] = keywords_file
        query_dict["source_website"] = source_en
        count = mongo.master_timeline_weibo.find(query_dict).count()
        results = mongo.master_timeline_weibo.find(query_dict)

        rs = []
        inputs = []
        for r in results:
            text = _encode_utf8(r['text'])
            inputs.append([r['_id'], text])
            rs.append(r)

        if len(inputs):
            rel = rel_classifier(inputs)
        else:
            rel = []            
        rel = [int(l) for l in rel]

        rel_count = 0
        for idx, r in enumerate(rs):
            if rel[idx] == 1:
                rel_count += 1
                rubbish = False
            else:
                rubbish = True
            
            mongo.master_timeline_weibo.update({"_id": r["_id"]}, {"$set": {"rubbish": rubbish}})
    else:
        query_dict["category"] = keywords_file
        query_dict["source_website"] = source_en
        count = mongo.boatcol.find(query_dict).count()
        results = mongo.boatcol.find(query_dict)

        rs = []
        inputs = []
        for r in results:
            title = _encode_utf8(r['title'])
            content168 = _encode_utf8(r['content168'])
            summary = _encode_utf8(r['summary'])

            text = title  + content168 + summary
            inputs.append([r['_id'], text])
            rs.append(r)

        if len(inputs):
            rel = rel_classifier(inputs)
        else:
            rel = []
        rel = [int(l) for l in rel]

        rel_count = 0
        for idx, r in enumerate(rs):
            if rel[idx] == 1:
                rel_count += 1
                rubbish = False
            else:
                rubbish = True
            
            mongo.boatcol.update({"_id": r["_id"]}, {"$set": {"rubbish": rubbish}})

    print source_en, keywords_file, count, rel_count

print "rubbish filter ends..."
