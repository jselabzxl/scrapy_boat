# -*- coding: utf-8 -*-

import os
import scws
import csv
import re
from svmutil import *

SCWS_ENCODING = 'utf-8'
SCWS_RULES = '/usr/local/scws/etc/rules.utf8.ini'
CHS_DICT_PATH = '/usr/local/scws/etc/dict.utf8.xdb'
CHT_DICT_PATH = '/usr/local/scws/etc/dict_cht.utf8.xdb'
IGNORE_PUNCTUATION = 1

ABSOLUTE_DICT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './dict'))
CUSTOM_DICT_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'userdic.txt')
EXTRA_STOPWORD_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'stopword.txt')
EXTRA_EMOTIONWORD_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'emotionlist.txt')
EXTRA_ONE_WORD_WHITE_LIST_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'one_word_white_list.txt')
EXTRA_BLACK_LIST_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'black.txt')

cx_dict = ['Ag','a','an','Ng','n','nr','ns','nt','nz','Vg','v','vd','vn','@']#关键词词性词典

def load_one_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_ONE_WORD_WHITE_LIST_PATH)]
    return one_words

def load_black_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_BLACK_LIST_PATH)]
    return one_words

single_word_whitelist = set(load_one_words())
single_word_whitelist |= set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')

def load_scws():
    s = scws.Scws()
    s.set_charset(SCWS_ENCODING)

    s.set_dict(CHS_DICT_PATH, scws.XDICT_MEM)
    s.add_dict(CHT_DICT_PATH, scws.XDICT_MEM)
    s.add_dict(CUSTOM_DICT_PATH, scws.XDICT_TXT)

    # 把停用词全部拆成单字，再过滤掉单字，以达到去除停用词的目的
    s.add_dict(EXTRA_STOPWORD_PATH, scws.XDICT_TXT)
    # 即基于表情表对表情进行分词，必要的时候在返回结果处或后剔除
    s.add_dict(EXTRA_EMOTIONWORD_PATH, scws.XDICT_TXT)

    s.set_rules(SCWS_RULES)
    s.set_ignore(IGNORE_PUNCTUATION)
    return s

def train():#生成训练集数据
    reader = csv.reader(file('./test/train.csv', 'rb'))
    feature = []
    lable = []
    text_data = []
    black = load_black_words()
    sw = load_scws()
    for title,text,flag in reader:
        lable.append(flag)
        text_data.append(text)
        words = sw.participle(text)
        for word in words:
            if (word[1] in cx_dict) and (3 < len(word[0]) < 30 or word[0] in single_word_whitelist):# and (word[0] not in black):#选择分词结果的名词、动词、形容词，并去掉单个词
                if word[0] not in feature:
                    feature.append(word[0])

    item = []
    for i in range(0,len(text_data)):
        row = ''
        row = row + lable[i]
        for j in range(0,len(feature)):
            if feature[j] in text_data[i]:
                row = row + ' ' + str(j+1) + ':' + str(text_data[i].count(feature[j]))        
        item.append(row)
    
    with open('./svm/train.txt', 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(item)):
            row = []
            row.append(item[i])
            writer.writerow((row))

    with open('./svm/feature.csv', 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(feature)):
            writer.writerow((i+1,feature[i]))                    

def test(weibo,flag):
    word_dict = dict()
    reader = csv.reader(file('./svm/feature.csv', 'rb'))
    for w,c in reader:
        word_dict[str(c)] = w 

    items = []
    sw = load_scws()
    for i in range(0,len(weibo)):
        words = sw.participle(weibo[i][1])
        row = dict()
        for word in words:
            if (word[1] in cx_dict) and (3 < len(word[0]) < 30 or word[0] in single_word_whitelist):
                if row.has_key(str(word[0])):
                    row[str(word[0])] = row[str(word[0])] + 1
                else:
                    row[str(word[0])] = 1
        items.append(row)


    f_items = []
    for i in range(0,len(items)):
        row = items[i]
        f_row = ''
        f_row = f_row + str(1)
        for k,v in word_dict.iteritems():
            if row.has_key(k):
                item = str(word_dict[k])+':'+str(row[k])
                f_row = f_row + ' ' + str(item) 
        f_items.append(f_row)

    with open('./svm_test/test%s.txt' % flag, 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(f_items)):
            row = []
            row.append(f_items[i])
            writer.writerow((row))
    f.close()
    return items

def cross_text():
    y, x = svm_read_problem('./svm/train.txt')
    m = svm_train(y, x, '-c 4  -v 10  -t 0')

def choose_ad(flag):
    y, x = svm_read_problem('./svm/train.txt')
    m = svm_train(y, x, '-c 4 -t 0')

    y, x = svm_read_problem('./svm_test/test%s.txt' % flag)
    p_label, p_acc, p_val  = svm_predict(y, x, m)

    return p_label

def start(flag):

    weibo_mid = []
    reader = csv.reader(file('./test/test%s.csv' % flag, 'rb'))
    for t,c in reader:
        weibo_mid.append([t,c]) 
    
    test(weibo_mid,flag)#生成测试数据
    
    lable = choose_ad(flag)#广告过滤   

    return lable

if __name__ == '__main__':
    lable = start('1')#生成训练集
    print lable
##    train()
##    cross_text()

