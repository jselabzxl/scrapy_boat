#-*-coding=utf-8-*-

import time
import pymongo

MONGOD_HOST = '219.224.135.46'
MONGOD_PORT = 27019

def _default_mongo(host=MONGOD_HOST, port=MONGOD_PORT, usedb='boat'):
    # 强制写journal，并强制safe
    connection = pymongo.MongoClient(host=host, port=port, j=True, w=1)
    db = connection.admin
    # db.authenticate('root', 'root')
    db = getattr(connection, usedb)
    return db

def get_module_keywords():
    f = open("../source/keywords_taxnomy.txt")

    results = []
    count = 0
    for line in f:
        if count == 0:
            count += 1
            continue

        bankuai, lanmu, source, source_en, keywords_file = line.strip().split()
        results.append((bankuai, lanmu, source, source_en, keywords_file))
        count += 1

    return results

def datetime2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

START_DATETIME = "2015-01-03 00:00:00"
END_DATETIME = "2015-01-10 00:00:00"
START_TS = datetime2ts(START_DATETIME)
END_TS = datetime2ts(END_DATETIME)
