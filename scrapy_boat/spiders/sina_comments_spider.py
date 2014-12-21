# -*- coding: utf-8 -*-

import re
import time
import json
from scrapy import log
from scrapy import Spider
from scrapy.http import Request
from BeautifulSoup import BeautifulSoup

LIST_URL = "http://comment5.news.sina.com.cn/comment/skin/default.html?channel=gn&newsid={newsid}"

class SinaCommentsSpider(Spider):
    """usage: scrapy crawl sina_comments --loglevel=INFO
    """
    name = "sina_comments"

    def __init__(self):
        self.newsid = "1-1-31285984"

    def start_requests(self):
        search_url = LIST_URL.format(newsid=self.newsid)
        log.msg(search_url)
        request = Request(search_url)
        request.meta['webkit'] = True

        yield request

    def parse(self, response):
        resp = response.body
        self.resp2items(resp)

    def resp2items(self, resp):
        soup = BeautifulSoup(resp)

        results = []
        comments = soup.findAll("div", {"class": "comment_item"})
        for comment in comments:
            log.msg('-----start')

            comment_id = comment.get("id")
            j_comment_face_t_face = comment.find("div", {"class": "J_Comment_Face t_face"})

            comment_a = j_comment_face_t_face.find("a")
            if comment_a:
                user_name = comment_a.get("title", None)
                user_url = comment_a.get("href", None)
                user_thumbnail_url = comment_a.find("img").get("src", None)
            else:
                user_name = None
                user_url = None
                user_thumbnail_url = j_comment_face_t_face.find("img").get("src")

            t_content_div = comment.find("div", {"class": "t_content"})

            J_Comment_Info = t_content_div.find("div", {"class": "J_Comment_Info"})
            t_info_div = J_Comment_Info.find("div", {"class": "t_info"})
            user_name_span_a = t_info_div.findAll("span")[0].find("a")
            if user_name_span_a:
                user_comment_url = user_name_span_a.get("href", None)
                user_name = user_name_span_a.text
            else:
                user_comment_url = None
                user_name = t_info_div.findAll("span")[0].text
            user_area = t_info_div.find("span", {"class": "t_area"}).text.lstrip('[').rstrip(']')

            J_Comment_Reply = t_content_div.find("div", {"class": "J_Comment_Reply"})
            orig_comments = []
            if J_Comment_Reply:
                comment_orig_content = J_Comment_Reply.find("div", {"class": "comment_orig_content"})
                if comment_orig_content:
                    orig_comments = self.orig_cont_parse(comment_orig_content, orig_comments)
            comment_index = len(orig_comments) + 1

            J_Comment_Txt = comment.find("div", {"class": "comment_content J_Comment_Txt clearfix"})
            comment_content = J_Comment_Txt.find("div", {"class": "t_txt"}).text
            reply = J_Comment_Txt.find("div", {"class": "reply"})
            timestamp = int(reply.find("span", {"class": "datetime J_Comment_Time"}).get("date")) / 1000
            attitudes_count = reply.find("span", {"class": "reply-right"}).find("a", {"class": "comment_ding_link"}).text.encode('utf-8').lstrip('支持(').rstrip(')')
            idstr = reply.find("span", {"class": "reply-right"}).find("a", {"class": "comment_ding_link"}).get("action-data")
            news_id = re.search(r'newsid=(.*?)&mid', idstr).group(1)
            comment_id = re.search(r'mid=(.*)', idstr).group(1)

            item = {"_id": comment_id, "id": comment_id, "newsid": news_id, "user_url": user_url, "user_thumbnail_url": user_thumbnail_url, "user_comment_url": user_comment_url, "user_name": user_name, "user_area": user_area, "content": comment_content, "timestamp": timestamp, "attitudes_count": attitudes_count, "orig_comments": orig_comments, "index": comment_index}

            print item

            log.msg('-----end')

    def orig_cont_parse(self, orig_cont, orig_comments):
        orig_cont_clearfix = orig_cont.find("div", {"class": "orig_cont clearfix"})

        if orig_cont_clearfix:
            orig_news_id = None
            orig_comment_id = None
            orig_index = None
            orig_content = None
            user_comment_url = None
            user_name = None
            user_area = None
            orig_timestamp = None
            orig_attitudes_count = None

            for div in orig_cont_clearfix.contents:
                div_class = div.get("class")
                if div_class == 'orig_cont clearfix':
                    orig_comments = self.orig_cont_parse(orig_cont_clearfix, orig_comments)
                elif div_class == 'orig_index':
                    orig_index = int(div.text)
                elif div_class == 'orig_user':
                    orig_user_div = div
                    user_name_span_a = orig_user_div.find("a")
                    if user_name_span_a:
                        user_comment_url = user_name_span_a.get("href", None)
                        user_name = user_name_span_a.text
                    else:
                        user_comment_url = None
                        user_name = orig_user_div.text.split('[')[0]
                    user_area = orig_user_div.find("span", {"class": "orig_area"}).text.lstrip('[').rstrip(']')
                elif div_class == 'orig_content':
                    orig_content = div.text
                elif div_class == 'orig_reply':
                    orig_reply = div
                    orig_timestamp = int(orig_reply.find("span", {"class": "orig_time J_Comment_Time"}).get("date")) / 1000
                    orig_attitudes_count = int(orig_reply.find("span", {"class": "reply-right"}).find("a", {"class": "comment_ding_link"}).text.encode('utf-8').lstrip('支持(').rstrip(')'))
                    idstr = orig_reply.find("span", {"class": "reply-right"}).find("a", {"class": "comment_ding_link"}).get("action-data")
                    orig_news_id = re.search(r'newsid=(.*?)&mid', idstr).group(1)
                    orig_comment_id = re.search(r'mid=(.*)', idstr).group(1)

            orig_comments.append({"_id": orig_comment_id, "id": orig_comment_id, "newsid": orig_news_id, "index": orig_index, "content": orig_content, "user_name": user_name, "user_comment_url": user_comment_url, "user_area": user_area, "timestamp": orig_timestamp, "attitudes_count": orig_attitudes_count})

        return orig_comments

