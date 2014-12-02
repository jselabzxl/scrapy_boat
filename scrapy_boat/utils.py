# -*- coding: utf-8 -*-

import time
import redis
import socket
import pymongo
import datetime
import simplejson as json

MONGOD_HOST = 'localhost'
MONGOD_PORT = 27017
REDIS_HOST = 'localhost'
REDIS_PORT = 6379


def _default_mongo(host=MONGOD_HOST, port=MONGOD_PORT, usedb='simple'):
    # 强制写journal，并强制safe
    connection = pymongo.MongoClient(host=host, port=port, j=True, w=1)
    db = connection.admin
    # db.authenticate('root', 'root')
    db = getattr(connection, usedb)
    return db


def _default_redis(host=REDIS_HOST, port=REDIS_PORT):
    return redis.Redis(host, port)


def datetime2str(dt):
      time_format = '%Y.%m.%d'
      return dt.strftime(time_format)


def local2unix(time_str):
    time_format = '%a %b %d %H:%M:%S +0800 %Y'
    return time.mktime(time.strptime(time_str, time_format))


def localIp():
    localIP = socket.gethostbyname(socket.gethostname())#得到本地ip
    print "local ip: %s " % localIP
    return localIP

