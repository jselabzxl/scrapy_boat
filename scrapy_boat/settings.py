# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_boat project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapy_boat'

SPIDER_MODULES = ['scrapy_boat.spiders']
NEWSPIDER_MODULE = 'scrapy_boat.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapy_boat (+http://www.yourdomain.com)'

SPIDER_MIDDLEWARES = {
    'scrapy_boat.middlewares.RetryErrorResponseMiddleware': 940
}

ITEM_PIPELINES = [
    'scrapy_boat.pipelines.MongodbPipeline'
]

DOWNLOADER_MIDDLEWARES = {
    #'scrapy_boat.middleware.WebkitDownloader': 1
}

BOAT_HOST = "219.224.135.46"
BOAT_PORT = 27019
BOAT_DB = "boat"
BOAT_COLLECTION = "boatcol"
WEIBO_COLLECTION = "master_timeline_weibo"
USER_COLLECTION = "master_timeline_user"
API_SERVER_HOST = "219.224.135.46"
API_SERVER_PORT = 9115
RETRY_TIMES = 3

