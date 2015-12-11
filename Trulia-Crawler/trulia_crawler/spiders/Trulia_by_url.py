# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

Remark: 1) If the result originally does not have feature records and features update date, then
            field "features_last_updated" will be relaced by the current date when the program
            is run.

Sample Usage:
    To run it on command line for parsing one link/url, run something like

>>> scrapy crawl Trulia_by_url --nolog -a start_url="http://www.trulia.com/property/3210700881-6-Bayberry-Ln-Worcester-MA-01602"
    , you may add "-o output.json" to output the result to the json file
"""


import numpy as np
import time
from scrapy.spiders import Spider
import re
from utils.load_settings import loadParameters
# the following is my own items in items.py, where from part is also the directory
    # of the items.py file
from trulia_crawler.items import housePageItem


def getUpdateDate(descpt,
            key_words_or=["county","public"],
            key_words_and=["as of","tax"]):
    """
    Search Key words and find the date for updated property info based on its description
    """
    key_words_or_1 = key_words_or
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
            #print("No Record As-Of Information is Provided")
            update_date = None
    else:
        #print("No Record As-Of Information is Provided")
        update_date = None
    return update_date


def findListwithHref(x):
    """ This program is to extract the bullet info with link embedded in the list """
    try:
        strings = re.findall(r"<li>\S*\s*\w*\s*\w*\s*\w*\w*\w*\s*<a href=",x)[0].replace("<a href=","").replace("<li>","")
        strings += re.findall(r">\w*\s*\w*\s*\w*\s*\w*\s*\w*\s*\w*\s*\w*\s*</a></li>", x)[-1].replace("</a></li>","").replace(">","")
        out = strings
    except:
        out = ""
    return out

def uniqueElem(mlist):
    """This function is just to eliminate the same element in the list"""
    x = np.array(mlist)
    return list(np.unique(x))

def removeDots(x):
    """ This function is to remove ... if they exist 
    for example, x= 'a...0bc', it should return a0bc
    but if x = 'a... 0bc', then keep it what it is
    """
    try:
        x2 = re.search(r'\w*\.\.\.\w',x).group(0)
        if x2.startswith('.'):
            x3 = x2
        else:
            x3 = re.search(r'\.\.\.\w',x2).group(0)
        x4 =x.replace(x3,x3[-1])
    except:
        x4 = x
        pass
    return x4

## Get current time stamp ##
def timeStamp():
    """returns a formatted current time/date"""
    #sample: 'Tue 18 Aug 2015 11:13:41 AM'
    #str(time.strftime("%a %d %b %Y %I:%M:%S %p"))
    return str(time.strftime("%m/%d/%Y"))

### Major Spyder Class ###

class truliaSpider(Spider):
    name = "Trulia_by_url"
    allowed_domains = ["www.trulia.com","trulia.com"]
    #start_urls = ('http://www.trulia.com/')
    def __init__(self, *args, **kwargs): 
        super(truliaSpider, self).__init__(*args, **kwargs) 
        self.start_urls = [kwargs.get('start_url')] 

    # this is for parsing the info given by response of website and start
        # parsing its contents
    def parse(self, response):
        self.logger.info('Parsing webpage %s ...', response.url)
        param = loadParameters()
        time.sleep(param['download_delay_for_web_crawling']) # for example, make download delay for 1 sec
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

        # get the property listing type, for sale, public record or foreclosure#
            #public records account for most of records since they are just homes 
            #having people live there and not for sale
        selectors = response.css('#propertyDetails div div')
        listing_type = []
        for selector in selectors:
            try:
                tpe = selector.xpath('text()').extract()[0]
                tpe = tpe.strip().replace('  ',' ')
                tpe = tpe.upper()
                listing_type.append(tpe)
            except:
                continue
        try:
            listing_type = filter(lambda x: len(x.strip()) >=3, listing_type)[0]
        except:
            listing_type = ""

        listing_type = listing_type.replace(u'\xb7','-')
        item['listing_type'] = listing_type

        # get basic property informatio on homepage
        try:
            selector_list = response.css('div#propertyDetails')
            selector = selector_list[0] # since we are only dealing with one property at a webpage
            propertylist = selector.xpath('//div/ul[contains(@class,"listBullet")]/li/text()').extract()
            propertylist_info = map(lambda x: x.strip().replace('  ',' '),propertylist)
            propertylist_info = filter(lambda x: len(x) >= 1, propertylist_info)
            item['property_basic_info'] = uniqueElem(propertylist_info)
        except:
            pass

        # get property description (as a statement) given by Trulia
        property_dscription_12 = ""
        property_dscription_22 = ""

        try:
            selector_list = response.css('span#corepropertydescription')
            selector = selector_list[0] # since we are only dealing with one property at a webpage
            property_dscription = selector.xpath('text()').extract()
            property_dscription_1 = filter(lambda x: len(x) > 0,map(lambda x: x.strip().replace('  ',' '), property_dscription))
            property_dscription_12 = "".join(property_dscription_1)
        except:
            pass
        try:
            selector_list = response.css('span#corepropertydescription')
            selector = selector_list[0]
            property_dscription = selector.xpath('span/text()').extract()
            property_dscription_1 = filter(lambda x: len(x) > 0,map(lambda x: x.strip().replace('  ',' '), property_dscription))
            property_dscription_22 = "".join(property_dscription_1)
            property_dscription_22 = property_dscription_22.strip()
            property_dscription_22 = removeDots(property_dscription_22)
        except:
            pass
        try:
            property_dscription = property_dscription_12 + property_dscription_22
        except:
            pass
        try:
            item['property_dscription'] = property_dscription
        except:
            pass

        # get property record by county
        try:
            selector_list = response.css('ul[class="listInline mbn pdpFeatureList"]')
            selector = selector_list[0] # since we are only dealing with one property at a webpage
            property_county_record = selector.xpath('li/ul/li/text()').extract()
            property_county_record = map(lambda x: x.strip().replace('  ',' '),property_county_record)
            property_county_record = filter(lambda x: len(x) >= 1, property_county_record)
            property_county_record = filter(lambda x: not(x.endswith(":") and x.count(":")==1), property_county_record)
        except:
            pass

        try:
            selector_list = response.css('ul[class="listInline mbn pdpFeatureList"]')
            selector = selector_list[0]
            property_county_record_2 = selector.xpath('li/ul/li').extract()
            property_county_record_2 = filter(lambda x: x.lower().find('<a href=')>=0, property_county_record_2)
            property_county_record_2 = map(findListwithHref, property_county_record_2)
            property_county_record_2 = filter(lambda x: len(x.strip())>=1, property_county_record_2)
            property_county_record += property_county_record_2
        except:
            pass
        try:
            item['property_county_record'] = uniqueElem(property_county_record)
        except:
            pass

        # get property record by features posted by other sources
        try:
            selector_list = response.css('ul[class="listInline pdpFeatureList"]')
            selector = selector_list[0] # since we are only dealing with one property at a webpage
            property_features_record = selector.xpath('li/ul/li/text()').extract()
            property_features_record = map(lambda x: x.strip().replace('  ',' '),property_features_record)
            property_features_record = filter(lambda x: len(x) >= 1, property_features_record)
            property_features_record = filter(lambda x: not(x.endswith(":") and x.count(":")==1), property_features_record)
        except:
            pass
        try:
            selector_list = response.css('ul[class="listInline pdpFeatureList"]')
            selector = selector_list[0]
            property_features_record_2 = selector.xpath('li/ul/li').extract()
            property_features_record_2 = filter(lambda x: x.lower().find('<a href=')>=0, property_features_record_2)
            property_features_record_2 = map(findListwithHref, property_features_record_2)
            property_features_record_2 = filter(lambda x: len(x.strip())>=1, property_features_record_2)
            property_features_record += property_features_record_2
        except:
            pass
        try:
            item['property_features_record'] = uniqueElem(property_features_record)
        except:
            pass

        # get property features & county record last updated time
        selector_list = response.css('div.line.asideFloaterContainer div.col.cols16 div.mtl')
        descpt = []
        for selector in selector_list:
            descpt += selector.xpath("span/text()").extract()
        descpt = map(lambda x: x.strip().replace('  ',' '),descpt)
        #descpt = filter(lambda x: len(x) > 2, descpt)
        descpt = filter(lambda x: (("information" in x.lower()) & ("updated" in x.lower()))
                        or (("official" in x.lower()) & ("county" in x.lower())), descpt)

        feature_Update_func = lambda x: getUpdateDate(x,
                        key_words_or=["last"],
                        key_words_and=["Information","updated"])
        county_Update_func = lambda x: getUpdateDate(x,
                        key_words_or=["county","public"],
                        key_words_and=["as of","tax"])
        features_last_updated = filter(lambda x: len(str(x))>2 and str(x)!='None', map(feature_Update_func,descpt))
        county_last_updated = filter(lambda x: len(str(x))>2 and str(x)!='None', map(county_Update_func,descpt))
        try:
            item['features_last_updated'] = features_last_updated[0]
        except:
            pass
        try:
            item['county_last_updated'] = county_last_updated[0]
        except:
            pass

        try:
            x_ = item['features_last_updated']
        except KeyError:
            item['features_last_updated'] = timeStamp()

        return item

