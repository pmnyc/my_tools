# -*- coding: utf-8 -*-
"""
@author: pm

Sample Usage:
import simple_scrapy_webcrawling
df = simple_scrapy_webcrawling.main(fpath = 'mywebpage.html', customer_data="mycustomer.csv",id=1234, scenario_id="5432abcd")
"""
from scrapy.selector import Selector
import pandas as pd, numpy as np
import calendar

def parseOneHtml(textstr, usage_year):
    # sample input:
    # usage_year = 2014
    datestr = ['1/1/2013', '2/1/2013', '3/1/2013', '4/1/2013', \
              '5/1/2013', '6/1/2013', '7/1/2013', '8/1/2013', \
              '9/1/2013', '10/1/2013', '11/1/2013', '12/1/2013']
    datestr = map(lambda t: t[:-4] + str(usage_year), datestr)
    TotalAmount=[]
    for p in Selector(text=textstr).xpath('/html/body/b'):
        if p.extract().find('MyTargetTable') >= 0:
            break
    t = p.xpath('following-sibling::table[1]')
    trpath = './/child::tbody/tr'
    if len(t.xpath('.//child::tbody').extract())==0:
        trpath='.//tr'
    #changed
    for tr in t.xpath(trpath):
    #for tr in t.xpath('.//tr'): #t.xpath('.//child::tbody/tr'):
        tx = tr.xpath('.//following-sibling::*')
        if len(tx[0].xpath('.//text()').extract())==0:
            continue
        if tx[0].extract().find('TotalAmount')>=0:
            for i in range(1,13):
                TotalAmount.append(float((tx[i].xpath('.//text()').extract())[0]))
    return pd.DataFrame.from_items( [('datestr',datestr), ('TotalAmount',TotalAmount)])

def getMonth(x):
    # for example:
    # x = '2/1/2014'
    return int(x.split("/")[0])

def getEndofMonth(x):
    # for example:
    # x = '2/1/2014'
    date = calendar.monthrange(int(x[-4:]),getMonth(x))[1]
    month = getMonth(x)
    year = int(x[-4:])
    return str(month) + "/" + str(date) + "/" + str(year)

if __name__ in ['__main__','simple_scrapy_webcrawling']:
    def main(fpath, customer_data, id, scenario_id, usage_year = 2014):
        # sample usage:
        fn = open(fpath,'r')
        text = fn.read()
        fn.close()
        #print text
        #res=scrapy.http.HtmlResponse('nullheader',body=text)
        df = parseOneHtml(text, usage_year)
        df2 = parseOneHtml(text, usage_year+1)
        df3 = pd.concat([df, df2], axis=1) #just put two table columns together side by side
        df=df.rename(columns = {'datestr':'date_from'}) #rename columns
        df['scenario_id'] = scenario_id
        
        customer_df = pd.read_csv(customer_data)
        customer_df.columns = map(lambda t: t.lower(),customer_df.columns)
        df2 = pd.merge(df, customer_df, how = 'inner')
        df2['var2'] = df2['factor'] * df2['var1']
        df['strangefield'] = np.nan
        return df