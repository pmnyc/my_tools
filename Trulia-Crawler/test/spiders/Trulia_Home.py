# -*- coding: utf-8 -*-
"""
@author: Man Peng

base crawler for the trulia.com

    We may use the following to check the validility of the regex string for matches used in the rules
        later on
    >>> import re
    >>> p ='homes/Massachusetts/Worcester/sold/1779200\S+'
    >>> x = re.match(p,'homes/Massachusetts/Worcester/sold/1779200-61-Edgeworth-St-Worcester-MA-01605')
    >>> print x.group(0) # this is for showing the match results

The parser here (function parse_item) only parses the webpages with link info of the format
    http://www.trulia.com/homes/Massachusetts/Worcester/sold/1779200-61-Edgeworth-St-Worcester-MA-01605

"""

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.sgml import SgmlLinkExtractor
import re
# the following is my own items in items.py, where from part is also the directory
    # of the items.py file
from trulia_crawler.items import housePageItem

def getUpdateDate(descpt):
    """
    Search Key words and find the date for updated property info based on its description
    """
    key_words_or_1 = ["county","public"]
    key_words_and = ["as of","tax"]
    match_keywords_or_1 = filter(lambda x: x.lower() in descpt.lower(),key_words_or_1)
    match_keywords_and = filter(lambda x: x.lower() in descpt.lower(),key_words_and)
    
    if len(match_keywords_or_1) >0 and len(match_keywords_and)==len(key_words_and):
        descpt = descpt.replace("(","").replace(")","").replace(":","").replace(",","")
        descpt = descpt.lower()
        update_date_1 = None
        update_date_0 = None
        try:
            update_date_1 = re.search(r'\d+/\d+',descpt).group(0)
        except AttributeError:
            pass
        try:
            update_date_0 = re.search(r'\d+/\d+/\d+',descpt).group(0)
        except AttributeError:
            pass
        if update_date_0 != None:
            update_date = update_date_0
        elif update_date_1 != None:
            update_date = update_date_1
        else:
            print("No Record As-Of Information is Provided")
            update_date = None
    else:
        print("No Record As-Of Information is Provided")
        update_date = None
    return update_date

class BasetruliaSpider(CrawlSpider):
    name = "Trulia_Home"
    allowed_domains = ["www.trulia.com",'trulia.com']
    start_urls = [
        'http://www.trulia.com/homes/Massachusetts/Worcester/sold/1786384-3-Boardman-St-Worcester-MA-01606' #change!!!!!
    ]
    # this is to set the download delayed for 1 second for avoiding too frequent queries
    download_delay = 1

    rules =[
        Rule(LinkExtractor(
                # sample link http://www.trulia.com/homes/Massachusetts/Worcester/sold/1779200-61-Edgeworth-St-Worcester-MA-01605
                # the string in allow= is in regex 
                allow=('/homes/\S+/\S+/sold/1786384\S*'), #change!!!!!
                deny=['subsection\.php']), # this is to defin the denied links matching this pattern
                callback='parse_item',
                follow=True)
    ]

    # this is for parsing the info given by response of website and start
        # parsing its contents
    def parse_item(self, response):
        self.logger.info('Parsing webpage %s ...', response.url)
        """
        This part of codes can be tested in the interactive shell before we put them
        here
            >>> scrapy shell https://www.reddit.com/r/pics
        after it is launched, then test the response using the following
            >>> response
            >>> response.css('div.thing') # might not be useable for many other webpages
            >>> response.xpath('//h1/text()') # or add .extract() at the end to see brief info
            >>> response.css('h1::text') # or add .extract() at the end to see the brief info
            >>> response.css('a').extract()
            >>> response.css('a[class="choice"]').extract()
            >>> selector = response.css('div.thing')[0]
            >>> selector.xpath('a[contains(@class, "thumbnail")]/@href').extract() #get the iamge urls
            >>> selector.xpath('div/p/a/text()').extract() #to get title for image
            >>> selector.xpath('a/@href').extract() #to get the url of news
        """
        selector_list = response.css('h1.h6')
        selector = selector_list[0] # since we are only dealing with one property at a webpage
        # The item keys must be first specified in the items.py file
        item = housePageItem()
        item['streetAddress'] = selector.xpath('span[contains(@itemprop,"streetAddress")]/text()').extract()[0]
        item['city'] = selector.xpath('//span').xpath('span[contains(@itemprop,"addressLocality")]/text()').extract()[0]
        item['state'] = selector.xpath('//span').xpath('span[contains(@itemprop,"addressRegion")]/text()').extract()[0]
        item['zipcode'] = selector.xpath('//span').xpath('span[contains(@itemprop,"postalCode")]/text()').extract()[0]

        # get basic property informatio on homepage
        try:
            selector_list = response.css('div#propertyDetails')
            selector = selector_list[0] # since we are only dealing with one property at a webpage
            propertylist = selector.xpath('//div/ul[contains(@class,"listBullet")]/li/text()').extract()
            propertylist_info = map(lambda x: x.strip().replace('  ',' '),propertylist)
            propertylist_info = filter(lambda x: len(x) >= 1, propertylist_info)
            item['property_basic_info'] = propertylist_info
        except:
            pass

        # get property description (as a statement) given by Trulia
        try:
            selector_list = response.css('span#corepropertydescription')
            selector = selector_list[0] # since we are only dealing with one property at a webpage
            property_dscription = selector.xpath('text()').extract()[0]
            property_dscription = property_dscription.strip().replace('  ',' ')
            item['property_dscription'] = property_dscription
        except:
            pass

        # get property record by county
        try:
            selector_list = response.css('ul.listInline.mbn.pdpFeatureList')
            selector = selector_list[0] # since we are only dealing with one property at a webpage
            property_county_record = selector.xpath('//li/ul/li/text()').extract()
            property_county_record = map(lambda x: x.strip().replace('  ',' '),property_county_record)
            property_county_record = filter(lambda x: len(x) >= 1, property_county_record)
            item['property_county_record'] = property_county_record
        except:
            pass

        # get property record last updated time
        selector_list = response.css('div.line.asideFloaterContainer')
        for selector in selector_list:
            descpt = selector.xpath('//div[contains(@class,"col cols16")]/div[contains(@class,"mtl")]/span/text()').extract()[0]
            descpt = descpt.strip().replace('  ',' ')
            if len(descpt) >= 2:
                break
        item['county_last_updated'] = getUpdateDate(descpt)
        return item
