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

ITEM_PIPELINES = [
    #'scrapy_boat.pipelines.ScrapyBoatPipeline',
    #'scrapy_boat.pipelines.WeixinCsvPipeline'
    'scrapy_boat.pipelines.ChuanrenCsvPipeline'
]
