export START_DATETIME_SCRAPY_BOAT="2014-11-29 00:00:00"
export END_DATETIME_SCRAPY_BOAT="2014-12-06 00:00:00"
echo $START_DATETIME_SCRAPY_BOAT
echo $END_DATETIME_SCRAPY_BOAT
scrapy crawl baidu_ns_search -a keywords_file='keywords_corp_baidu.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl weibo_api_search_spider -a keywords_file='keywords_corp_weiboapi.txt' --loglevel=INFO
scrapy crawl xinhua_bbs_search -a keywords_file='keywords_corp_forum.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl tianya_bbs_search -a keywords_file='keywords_corp_forum.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl sogou_weixin_search -a keywords_file='keywords_corp_weixin.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl baidu_ns_search -a keywords_file='keywords_leader_baidu.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl weibo_api_search_spider -a keywords_file='keywords_leader_weiboapi.txt' --loglevel=INFO
scrapy crawl xinhua_bbs_search -a keywords_file='keywords_leader_forum.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl tianya_bbs_search -a keywords_file='keywords_leader_forum.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl sogou_weixin_search -a keywords_file='keywords_leader_weixin.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl baidu_ns_search -a keywords_file='keywords_hot_baidu.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl weibo_api_search_spider -a keywords_file='keywords_hot_weiboapi.txt' --loglevel=INFO
scrapy crawl xinhua_bbs_search -a keywords_file='keywords_hot_forum.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl tianya_bbs_search -a keywords_file='keywords_hot_forum.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --logleve    l=INFO
scrapy crawl sogou_weixin_search -a keywords_file='keywords_leader_weixin.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl baidu_ns_search -a keywords_file='keywords_enemy_baidu.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl weibo_api_search_spider -a keywords_file='keywords_enemy_weiboapi.txt' --loglevel=INFO
scrapy crawl xinhua_bbs_search -a keywords_file='keywords_enemy_forum.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl tianya_bbs_search -a keywords_file='keywords_enemy_forum.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl sogou_weixin_search -a keywords_file='keywords_enemy_weixin.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl baidu_ns_search -a keywords_file='keywords_friends_baidu.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl weibo_api_search_spider -a keywords_file='keywords _friends_weiboapi.txt' --loglevel=INFO
scrapy crawl xinhua_bbs_search -a keywords_file='keywords_friends_forum.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl tianya_bbs_search -a keywords_file='keywords_friends_forum.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl sogou_weixin_search -a keywords_file='keywords_friends_weixin.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl baidu_ns_search -a keywords_file='keywords_domain_baidu.txt' -a start_datetime=$START_DATETIME_SCRAPY_BOAT -a end_datetime=$END_DATETIME_SCRAPY_BOAT --loglevel=INFO
scrapy crawl weibo_api_search_spider -a keywords_file='keywords_domain_weiboapi.txt' --loglevel=INFO
