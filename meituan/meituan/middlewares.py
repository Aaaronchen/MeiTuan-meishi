# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
# Author AaaronChen
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random,requests,time
from scrapy.utils.project import get_project_settings

class CookiesMiddleware(object):
    def process_request(self,request,spider):
        #cookie = random.choice(get_cookie_from_mongodb())
        settings = get_project_settings()
        COOKIES = settings.get("COOKIES")
        cookie ={}
        for line in COOKIES.split(';'):
            key,value = line.split('=',1)
            cookie[key] = value
        request.cookies = cookie


class MyProxieswMiddleware(object):

    def process_request(self, request, spider):
        print("----------"*20)
        print('调用随机ip代理')
        proxy = self.get_proxy()
        request.meta['proxy'] ='http://' + proxy

    def process_response(self, request, response, spider):
        if response.status != 200:
            print("###########403重新请求中##########")
            proxy = self.get_proxy()
            request.meta['proxy'] ='http://' + proxy 
            return request     
        return response

    def process_exception(self, request, exception, spider):
        print("出现异常，正在使用代理重试...\n")
        proxy = self.get_proxy()
        request.meta['proxy'] ='http://' + proxy 
        return request

    def get_proxy(self):
        settings = get_project_settings()
        url = settings.get("PROXY_URL")
        res = requests.get(url = url).text
        if res:
            return res
        print('重新尝试获取代理...!!')
        time.sleep(1)
        return self.get_proxy()


class MeituanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MeituanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
