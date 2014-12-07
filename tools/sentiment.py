#-*-coding=utf-8-*-

import csv
import json
import collections
from xapian_case.utils import load_scws, cut
from triple_sentiment_classifier import triple_classifier
import csv

s = load_scws()

import time
def datetime2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M')))

def datetimestr2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

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

start_date = '2014-11-01 00:00'
end_date = '2014-11-22 00:00'
start_ts = datetime2ts(start_date)
end_ts = datetime2ts(end_date)
weibo_list = []
# files_list = ['items_search_corp.jl', 'items_search_leader.jl', 'items_search_hot.jl']
files_list = ['items_corp_20141115_20141121.csv', 'items_leader_20141115_20141121.csv', 'items_hot_20141115_20141121.csv']
for fs in files_list:
    #f = open(fs)
    reader = csv.reader(open(fs))
    for line in reader:
        #item = json.loads(line.strip())
        
        #if 'reposts_count' in item and item['timestamp'] >= start_ts and item['timestamp'] <= end_ts:
        #    weibo_list.append(item)
        item = {}
        item['text'] = line[1].decode('utf-8')
        weibo_list.append(item)

    #f.close()

"""
sorted_results = sorted(weibo_list, key=lambda k:k['reposts_count'], reverse=True)
f = open('weibo.csv', 'w')
for weibo in sorted_results:
    f.write('%s^%s^%s^%s\^%s^%s\n' % (weibo['timestamp'], weibo['created_at'].encode('utf-8'), weibo['user']['name'].encode('utf-8'), weibo['text'].encode('utf-8'), weibo['reposts_count'], weibo['attitudes_count']))


reader = csv.reader(file('forum_data.csv', 'rb'))
tcount = 0
fw = open("forum.csv", "w")
for line in reader:
    try:
        id, url, website, title, author, text, date, clicks, replies, label = line
        try:
            ts = datetime2ts(date)
        except:
            ts = datetimestr2ts(date)

        if ts > start_ts and ts < end_ts:
            tcount += 1
            fw.write("%s^%s^%s^%s^%s^%s^%s^%s^%s^%s\n" % (id, url, website, title, author, \
                text, date, clicks, replies, label))
            #weibo_list.append({'text': text.decode('utf-8') + title.decode('utf-8')})
    except:
        continue
print tcount
"""
print len(weibo_list)

sentiment_count = {}
tk = []
fw = open('negative_sentiment.txt', 'w')
for item in weibo_list:
    keywords = cut(s, item['text'].encode('utf-8'))
    tk.extend(keywords)
    item['sentiment'] = diamond_classifier(item)
    if item['sentiment'] == 2:
        fw.write('%s^%s\n' % (2, item['text'].encode('utf-8')))
    if item['sentiment'] == 3:
        fw.write('%s^%s\n' % (3, item['text'].encode('utf-8')))
    try:
        sentiment_count[item['sentiment']] += 1
    except:
        sentiment_count[item['sentiment']] = 1

print sentiment_count

"""
ct = collections.Counter(tk)
results = ct.most_common(50)
f = open('keywords_sheqi_forum.txt', 'w')
for k, v in results:
    print k, v
    f.write('%s\t%s\n' % (k, v))
f.close()
"""
