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

def get_s(text,weibo):#计算相似度，剔除重复文本

    max_r = 0
    n = -1
    for i in range(0,len(text)):
        r = Levenshtein.ratio(str(text[i][1]), str(weibo))
        if max_r <= r:
            max_r = r
            n = i
        else:
            pass
    return max_r,n

def test_weibo(flag):

    data = []
    number = dict()
    reader = csv.reader(file('./items_%s.csv' % flag, 'rb'))
    for mid,t,publish,a,b,c in reader:
        r,n = get_s(data,t)
        if r < 0.8:
            data.append([mid,t,publish,a,b,c])
            if number.has_key(n):
                number[n] = number[n] + 1
            else:
                number[n] = 1

    with open('./data%s.csv' % flag, 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(data)):
            if number.has_key(i):
                writer.writerow((data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5],number[i]))
            else:
                writer.writerow((data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5],0))

if __name__ == '__main__':
##    test_weibo('hot_20141115_20141121')
##    test_weibo('domain_20141115_20141121')
    test_weibo('enemy_20141115_20141121')
    #main('enemy')
