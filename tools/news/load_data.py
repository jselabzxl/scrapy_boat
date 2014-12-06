# -*- coding: utf-8 -*-

import os
import json
import csv
import time
import re
import datetime
from datetime import datetime
from datetime import date
import Levenshtein

def datetime2time(publish):#时间转换
    
    p_time = time.mktime(time.strptime(str(publish), '%Y-%m-%d %H:%M:%S'))
    return p_time

def get_s(text,weibo):#计算相似度，剔除重复文本

    max_r = 0
    n = -1
    for i in range(0,len(text)):
        r = Levenshtein.ratio(str(text[i]['summary'].encode('utf-8')), str(weibo.encode('utf-8')))
        if max_r <= r:
            max_r = r
            n = i
        else:
            pass
    return max_r,n

def main(flag):

    f = open('./items_%s.jl' % flag)
    start_time = datetime2time('2014-11-15 00:00:00')
    end_time = datetime2time('2014-11-22 00:00:00')

    data = []
    number = dict()
    for line in f:
        try:
            item = json.loads(line.strip())
        except:
            continue
        time_date = item['datetime']
        ts_time = datetime2time(time_date)
        if (int(ts_time) >= int(start_time)) and (int(ts_time) <= int(end_time)):
            r,n = get_s(data,item['summary'])
            if r < 0.8:
                data.append(item)
                if number.has_key(n):
                    number[n] = number[n] + 1
                else:
                    number[n] = 1

    with open('./data%s.csv' % flag, 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(data)):
            if number.has_key(i):
                writer.writerow((i+1,data[i]['same_news_num'],data[i]['author'].encode('utf-8'),data[i]['url'],data[i]['more_same_link'],data[i]['title'].encode('utf-8'),data[i]['relative_news'],data[i]['datetime'],data[i]['summary'].encode('utf-8'),number[i]))
            else:
                writer.writerow((i+1,data[i]['same_news_num'],data[i]['author'].encode('utf-8'),data[i]['url'],data[i]['more_same_link'],data[i]['title'].encode('utf-8'),data[i]['relative_news'],data[i]['datetime'],data[i]['summary'].encode('utf-8'),0))


if __name__ == '__main__':
    main('enemy')
