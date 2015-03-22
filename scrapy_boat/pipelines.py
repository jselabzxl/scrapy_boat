 # -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import json
import time
import pymongo
from scrapy import log
from utils import _default_mongo
from items import ChuanrenItem, ScrapyBoatItem, WeiboItem, UserItem, HaishiItem, GuochuanItem, ScrapyRenwuItem, ZhengyiItem
from twisted.internet.threads import deferToThread

class ScrapyBoatPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'ab')

    def process_item(self, item, spider):
        line = json.dumps(item.to_dict()) + "\n"
        self.file.write(line)
        return item

class WeixinCsvPipeline(object):
    def __init__(self):
        self.file = open('items.csv', 'w')

    def process_item(self, item, spider):
        csv_writer = csv.writer(self.file)
        csv_row = []
        for key in WeixinItem.RESP_ITER_KEYS:
            if item[key]:
                csv_row.append(item[key].replace("\ue468", "").encode('utf-8'))
            else:
                csv_row.append(item[key])

        csv_writer.writerow(csv_row)

        return item

# class ChuanrenCsvPipeline(object):
#     def __init__(self):
#         self.file = open('items.csv', 'w')

#     def process_item(self, item, spider):
#         csv_writer = csv.writer(self.file)
#         csv_row = []
#         for key in ChuanrenItem.RESP_ITER_KEYS_CHUANREN_NEWS:
#             if isinstance(item[key], unicode):
#                 csv_row.append(item[key].encode('utf-8'))
#             else:
#                 csv_row.append(item[key])

#         csv_writer.writerow(csv_row)

#         return item 

class MongodbPipeline(object):
    def __init__(self, db, host, port, collection, user_collection, weibo_collection):
        self.db_name = db
        self.host = host
        self.port = port
        self.db = _default_mongo(host, port, usedb=db)
        self.collection = collection
        self.user_collection = user_collection
        self.weibo_collection = weibo_collection
        log.msg('Mongod connect to {host}:{port}:{db}:{collection}'.format(host=host, port=port, db=db, collection=collection), level=log.INFO)

    @classmethod
    def from_settings(cls, settings):
        db = settings.get('BOAT_DB', None)
        host = settings.get('BOAT_HOST', None)
        port = settings.get('BOAT_PORT', None)
        boat_collection = settings.get('BOAT_COLLECTION', None)
        user_collection = settings.get('USER_COLLECTION', None)
        weibo_collection = settings.get('WEIBO_COLLECTION', None)
        return cls(db, host, port, boat_collection, user_collection, weibo_collection)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        if isinstance(item, ScrapyBoatItem):
            return deferToThread(self.process_boat, item, spider)
        if isinstance(item, WeiboItem):
            return deferToThread(self.process_weibo, item, spider)
        if isinstance(item, UserItem):
            return deferToThread(self.process_user, item, spider)
        if isinstance(item, ChuanrenItem):
            return deferToThread(self.process_chuanren, item, spider)
        if isinstance(item, HaishiItem):
            return deferToThread(self.process_haishi, item, spider)
        if isinstance(item, GuochuanItem):
            return deferToThread(self.process_guochuan, item, spider)
        if isinstance(item,ScrapyRenwuItem):
            return deferToThread(self.process_renwu, item, spider)
        if isinstance(item,ZhengyiItem):
            return deferToThread(self.process_zhengyi, item, spider)

    def update_boat(self, collection, boat_item):
        updates = {}
        updates['last_modify'] = time.time()
        for k, v in boat_item.iteritems():
            updates[k] = v

        updates_modifier = {'$set': updates}
        self.db[collection].update({'_id': boat_item['_id']}, updates_modifier)

    def update_chuanren(self, collection, chuanren_item):
        updates = {}
        updates['last_modify'] = time.time()
        for k, v in chuanren_item.iteritems():
            updates[k] = v

        updates_modifier = {'$set': updates}
        self.db[collection].update({'_id': chuanren_item['_id']}, updates_modifier)

    def update_haishi(self, collection, haishi_item):
        updates = {}
        updates['last_modify'] = time.time()
        for k, v in haishi_item.iteritems():
            updates[k] = v

        updates_modifier = {'$set': updates}
        self.db[collection].update({'_id': haishi_item['_id']}, updates_modifier)

    def update_guochuan(self, collection, guochuan_item):
        updates = {}
        updates['last_modify'] = time.time()
        for k, v in guochuan_item.iteritems():
            updates[k] = v

        updates_modifier = {'$set': updates}
        self.db[collection].update({'_id': guochuan_item['_id']}, updates_modifier)


    def update_zhengyi(self, collection, zhengyi_item):
        updates = {}
        updates['last_modify'] = time.time()
        for k, v in zhengyi_item.iteritems():
            updates[k] = v

        updates_modifier = {'$set': updates}
        self.db[collection].update({'_id': zhengyi_item['_id']}, updates_modifier)

    def update_renwu(self, collection, renwu_item):
        updates = {}
        updates['last_modify'] = time.time()
        for k, v in renwu_item.iteritems():
            updates[k] = v

        updates_modifier = {'$set': updates}
        self.db[collection].update({'_id': renwu_item['_id']}, updates_modifier)

    def process_boat(self, item, spider):
        boat_item = item.to_dict()

        hit = False
        if boat_item['id']:
            boat_item['_id'] = boat_item['id']

            if self.db[self.collection].find({'_id': boat_item['_id']}).count():
                hit = True

        if hit:
            self.update_boat(self.collection, boat_item)
        else:
            try:
                boat_item['first_in'] = time.time()
                boat_item['last_modify'] = boat_item['first_in']
                self.db[self.collection].insert(boat_item)
            except pymongo.errors.DuplicateKeyError:
                self.update_boat(self.collection, boat_item)

        return item

    def process_chuanren(self, item, spider):       
        chuanren_item = item.to_dict()

        hit = False
        if  chuanren_item['id']:
            chuanren_item['_id'] = chuanren_item['id']

            if self.db[self.collection].find({'_id': chuanren_item['_id']}).count():
                hit = True

        if hit:
            self.update_chuanren(self.collection, chuanren_item)
        else:
            try:
                chuanren_item['first_in'] = time.time()
                chuanren_item['last_modify'] = chuanren_item['first_in']
                self.db[self.collection].insert(chuanren_item)
            except pymongo.errors.DuplicateKeyError:
                self.update_chuanren(self.collection, chuanren_item)

        return item

    def process_renwu(self, item, spider):       
        renwu_item = item.to_dict()

        hit = False
        if  renwu_item['id']:
            renwu_item['_id'] = renwu_item['id']

            if self.db[self.collection].find({'_id': renwu_item['_id']}).count():
                hit = True

        if hit:
            self.update_renwu(self.collection, renwu_item)
        else:
            try:
                renwu_item['first_in'] = time.time()
                renwu_item['last_modify'] = renwu_item['first_in']
                self.db[self.collection].insert(renwu_item)
            except pymongo.errors.DuplicateKeyError:
                self.update_renwu(self.collection, renwu_item)

        return item

    def process_haishi(self, item, spider):       
        haishi_item = item.to_dict()

        hit = False
        if  haishi_item['id']:
            haishi_item['_id'] = haishi_item['id']

            if self.db[self.collection].find({'_id': haishi_item['_id']}).count():
                hit = True

        if hit:
            self.update_haishi(self.collection, haishi_item)
        else:
            try:
                haishi_item['first_in'] = time.time()
                haishi_item['last_modify'] = haishi_item['first_in']
                self.db[self.collection].insert(haishi_item)
            except pymongo.errors.DuplicateKeyError:
                self.update_haishi(self.collection, haishi_item)

        return item

    def process_guochuan(self, item, spider):       
        guochuan_item = item.to_dict()

        hit = False
        if  guochuan_item['id']:
            guochuan_item['_id'] = guochuan_item['id']

            if self.db[self.collection].find({'_id': guochuan_item['_id']}).count():
                hit = True

        if hit:
            self.update_guochuan(self.collection, guochuan_item)
        else:
            try:
                guochuan_item['first_in'] = time.time()
                guochuan_item['last_modify'] = guochuan_item['first_in']
                self.db[self.collection].insert(guochuan_item)
            except pymongo.errors.DuplicateKeyError:
                self.update_guochuan(self.collection, guochuan_item)

        return item

    def process_zhengyi(self, item, spider):       
        zhengyi_item = item.to_dict()

        hit = False
        if  zhengyi_item['id']:
            zhengyi_item['_id'] = zhengyi_item['id']

            if self.db[self.collection].find({'_id': zhengyi_item['_id']}).count():
                hit = True

        if hit:
            self.update_zhengyi(self.collection, zhengyi_item)
        else:
            try:
                zhengyi_item['first_in'] = time.time()
                zhengyi_item['last_modify'] = zhengyi_item['first_in']
                self.db[self.collection].insert(zhengyi_item)
            except pymongo.errors.DuplicateKeyError:
                self.update_zhengyi(self.collection, zhengyi_item)

        return item

    def update_weibo(self, weibo_collection, weibo):
        updates = {}
        updates['last_modify'] = time.time()
        for key in WeiboItem.PIPED_UPDATE_KEYS:
            if weibo.get(key) is not None:
                updates[key] = weibo[key]

        updates_modifier = {'$set': updates}
        self.db[weibo_collection].update({'_id': weibo['_id']}, updates_modifier)

    def process_weibo(self, item, spider):
        weibo = item.to_dict()
        weibo['_id'] = weibo['id']
        weibo['uid'] = weibo['user']['id']

        if self.db[self.weibo_collection].find({'_id': weibo['_id']}).count():
            self.update_weibo(self.weibo_collection, weibo)
        else:
            try:
                weibo['first_in'] = time.time()
                weibo['last_modify'] = weibo['first_in']
                self.db[self.weibo_collection].insert(weibo)
            except pymongo.errors.DuplicateKeyError:
                self.update_weibo(self.weibo_collection, weibo)

        return item

    def update_user(self, user_collection, user):
        updates = {}
        updates['last_modify'] = time.time()
        for key in UserItem.PIPED_UPDATE_KEYS:
            if user.get(key) is not None:
                updates[key] = user[key]

        updates_modifier = {'$set': updates}
        self.db[user_collection].update({'_id': user['_id']}, updates_modifier)

    def process_user(self, item, spider):
        user = item.to_dict()
        user['_id'] = user['id']
        if self.db[self.user_collection].find({'_id': user['_id']}).count():
            self.update_user(self.user_collection, user)
        else:
            try:
                user['first_in'] = time.time()
                user['last_modify'] = user['first_in']
                self.db[self.user_collection].insert(user)
            except pymongo.errors.DuplicateKeyError:
                self.update_user(self.user_collection, user)

        return item
