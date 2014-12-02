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
from items import ChuanrenItem, ScrapyBoatItem
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

class ChuanrenCsvPipeline(object):
    def __init__(self):
        self.file = open('items.csv', 'w')

    def process_item(self, item, spider):
        csv_writer = csv.writer(self.file)
        csv_row = []
        for key in ChuanrenItem.RESP_ITER_KEYS:
            if isinstance(item[key], unicode):
                csv_row.append(item[key].encode('utf-8'))
            else:
                csv_row.append(item[key])

        csv_writer.writerow(csv_row)

        return item

class WeixinSearchCsvPipeline(object):
    def __init__(self):
        self.file = open('items.csv', 'w')

    def process_item(self, item, spider):
        csv_writer = csv.writer(self.file)
        csv_row = []
        for key in WeixinSearchItem.RESP_ITER_KEYS:
            if isinstance(item[key], unicode):
                csv_row.append(item[key].encode('utf-8'))
            else:
                csv_row.append(item[key])

        csv_writer.writerow(csv_row)

        return item

class MongodbPipeline(object):
    def __init__(self, db, host, port, collection):
        self.db_name = db
        self.host = host
        self.port = port
        self.db = _default_mongo(host, port, usedb=db)
        self.collection = collection
        log.msg('Mongod connect to {host}:{port}:{db}:{collection}'.format(host=host, port=port, db=db, collection=collection), level=log.INFO)

    @classmethod
    def from_settings(cls, settings):
        db = settings.get('BOAT_DB', None)
        host = settings.get('BOAT_HOST', None)
        port = settings.get('BOAT_PORT', None)
        boat_collection = settings.get('BOAT_COLLECTION', None)
        return cls(db, host, port, boat_collection)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        if isinstance(item, ScrapyBoatItem):
            return deferToThread(self.process_boat, item, spider)

    def update_boat(self, collection, boat_item):
        updates = {}
        updates['last_modify'] = time.time()
        for k, v in boat_item.iteritems():
            updates[k] = v

        updates_modifier = {'$set': updates}
        self.db[collection].update({'_id': boat_item['_id']}, updates_modifier)

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

