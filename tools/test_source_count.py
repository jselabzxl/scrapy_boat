#-*-coding=utf-8-*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import csv
import time
import collections
from xapian_case.utils import load_scws, cut
from utils import START_DATETIME, END_DATETIME, _default_mongo, get_module_keywords, START_TS, END_TS


mongo = _default_mongo()

query_dict = {
    "datetime": {
        "$gte": "2014-11-06 00:00:00",
        "$lt": "2014-12-06 00:00:00"
    },
    "keywords_hit": True,
    "rubbish": False,
}

query_dict["$or"] = [{"category": "keywords_corp_baidu.txt"}, {"category": "keywords_hot_baidu.txt"}, {"category": "keywords_leader_baidu.txt"}]
query_dict["source_website"] = "baidu_ns_search"
count = mongo.boatcol.find(query_dict).count()
results = mongo.boatcol.find(query_dict)

source = {}
for r in results:
    try:
        source[r['user_name']] += 1
    except KeyError:
        source[r['user_name']] = 1
print len(source)


source_list = sorted(source.iteritems(),key=lambda(k, v):v,reverse=True)
result_source = [(k,v) for k, v in source_list]

with open('./news_source(1106-1206).txt','w')as fw:
    for k, v in result_source:
        fw.write(u'%s,%s\r\n'%(k, v))
