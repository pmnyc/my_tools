# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
This program defines the Download Middleware behaviour for crawler object
"""

import random
from scrapy.exceptions import IgnoreRequest
from scrapy.downloadermiddleware.httpproxy import HttpProxyMiddleware


# set the proxy
class ConditionalProxyMiddleware(HttpProxyMiddleware):
    def process_request(self, request, spider):
        if getattr(spider, 'use_proxy', None):
            return super(ConditionalProxyMiddleware, self).process_request(request, spider)


## random roation of user agent setting
class RandomUserAgent(object):
    """
    Randomly rotate user agents based on a list of predefined ones
    This program is used in the settings.py to specify the download middleware 
        download behaviour
    """

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))


class ErrorMonkeyMiddleware(object):

    def process_request(self, request, spider):
        if 'x-ignore-request' in request.url:
            raise IgnoreRequest()
        elif 'x-error-request' in request.url:
            _ = 1 / 0

    def process_response(self, request, response, spider):
        if 'x-ignore-response' in request.url:
            raise IgnoreRequest()
        elif 'x-error-response' in request.url:
            _ = 1 / 0
        else:
            return response
