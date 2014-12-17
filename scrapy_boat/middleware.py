#-*-coding=utf-8-*-

import cwebbrowser
from scrapy.http import HtmlResponse

class WebkitDownloader(object):
    def process_request(self, request, spider):
        timeout = 10
        delay = 3
        headers = {}
        if 'webkit' in request.meta and request.meta['webkit'] == True:
            browser = cwebbrowser.CWebBrowser()
            browser.setHeaders(headers)
            #browser.show();
            try:
                browser.load(url=url, load_timeout=timeout, delay=delay)
            except cwebbrowser.Timeout:
                pass
            except Exception, exception:
                print "Exception message:", exception

            else:
                html = browser.html()
                if html:
                    html = html.encode('utf-8')
                else:
                    pass

            browser.close()
            return HtmlResponse(url, encoding='utf-8', body=html)

