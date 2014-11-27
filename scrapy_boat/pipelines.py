# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import json
from items import WeixinItem, ChuanrenItem

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
