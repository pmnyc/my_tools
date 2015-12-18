# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
@author: Man Peng

This is the main parser of the webpage.


Sample Usage:
content here is content of hmtl file

>>> from app import parser
>>> obj = parser.Parser(content)
>>> physical_address = obj.getLocation()
>>> building_area = obj.getBuildingAreas() # here building_area is a dictionary
>>> building_attributes = obj.getBuildingAttributes() # also a dictionary
"""

from scrapy.selector import Selector
#import pandas as pd, numpy as np
#import calendar

def openHtmlfile(file_):
    f = open(file_, "r")
    content = f.read()
    return content

class Parser(object):
    """ This is the code for parsing the webpage 
        for scraping property information 
    content is the html information
    """
    def __init__(self, content):
        #super(ClassName, self).__init__()
        self.content = content
    
    ## The following are individual parsers for scraping webpage
    def getTown(self):
        p = Selector(text=self.content).xpath('//*[@id="lblTownName"]/text()')
        town = p.extract()[0]
        town = town.replace(",", ", ").replace("  "," ").title().strip()
        town = town[:-2] + town[-2:].upper()
        return town

    def getLocation(self):
        """ This is the physical address """
        p = Selector(text=self.content).xpath('//*[@id="MainContent_rowLocation"] \
                    /dd/span[@id="MainContent_lblLocation"]/text()')
        try:
            location = p.extract()[0]
            location = location.title()
        except IndexError:
            print("The Location Information is empty!")
            return ""
        return location + ", " + self.getTown()

    def getAddress(self):
        """ The address is the owner address, not ncessary to be physical address """
        p = Selector(text=self.content).xpath('//*[@id="MainContent_lblAddr1"]/text()')
        address1 = ", ".join(p.extract())
        address2 = address1.split(",")
        address2 = map(lambda t: t.replace("  "," ").strip().title(), address2)
        address3 = address2[:-1] + [address2[-1].upper()]
        return ", ".join(address3)

    def getMapLot(self):
        """ Obtain the Map Lot Lotcut Unit"""
        p = Selector(text=self.content).xpath('//*[@id="MainContent_lblMblu"]/text()')
        try:
            maplot = p.extract()[0]
        except IndexError:
            print("No Map Lot Locut Unit information is available for %s" % self.getLocation())
            return ""
        #maplot = maplot.strip()
        return maplot

    def getOwner(self):
        """ Obtain the Owner of the property/parcel """
        p = Selector(text=self.content).xpath('//*[@id="MainContent_lblGenOwner"]/text()')
        try:
            owner = p.extract()[0]
        except IndexError:
            print("No Owner information is available for %s" % self.getLocation())
            return ""
        return owner

    def getAccountNum(self):
        """ Obtain the Account number for this property or parcel """
        p = Selector(text=self.content).xpath('//*[@id="MainContent_lblAcctNum"]/text()')
        try:
            accountnum = p.extract()[0]
        except IndexError:
            print("No Account Number information is available for %s" % self.getLocation())
            return ""
        return accountnum

    def getPID(self):
        """ Obtain the PID for this property or parcel """
        p = Selector(text=self.content).xpath('//*[@id="MainContent_lblPid"]/text()')
        try:
            pid = p.extract()[0]
        except IndexError:
            print("No PID information is available for %s" % self.getLocation())
            return ""
        return pid

    def getAssessment(self):
        """ Obtain the Assessment for this property or parcel """
        p = Selector(text=self.content).xpath('//*[@id="MainContent_lblGenAssessment"]/text()')
        try:
            assessment = p.extract()[0]
        except IndexError:
            print("No Assessment information is available for %s" % self.getLocation())
            return ""
        return assessment

    def getBuildingCount(self):
        """ Obtain the BuildingCount for this property or parcel """
        p = Selector(text=self.content).xpath('//*[@id="MainContent_lblBldCount"]/text()')
        try:
            buildingcount = p.extract()[0]
        except IndexError:
            print("No Building Count information is available for %s" % self.getLocation())
            return ""
        return buildingcount

    def getFireDistrict(self):
        """ Obtain the FireDistrict for this property or parcel """
        p = Selector(text=self.content).xpath('//*[@id="MainContent_lblUf05"]/text()')
        try:
            firedistrict = p.extract()[0]
        except IndexError:
            print("No Fire District is available for %s" % self.getLocation())
            return ""
        return firedistrict

    def getYearBuilt(self):
        """ Obtain the YearBuilt for this property or parcel """
        p = Selector(text=self.content).xpath('//*[@id="MainContent_ctl01_lblYearBuilt"]/text()')
        try:
            yearbuilt = p.extract()[0]
        except IndexError:
            print("No Year Built is available for %s" % self.getLocation())
            return ""
        return yearbuilt

    def getBuildingAttributes(self):
        """ Obtain the Building Attributes for this property or parcel 
            The results of this function are in a dictionary
        """
        def statusSwitch(status):
            if status == 'field':
                return 'value'
            elif status == 'value':
                return 'field'
            else:
                raise Exception('Status has to be either field or value')

        p = Selector(text=self.content).xpath('//*[@id="MainContent_ctl01_grdCns"]/tbody/tr/td/text()')
        table = p.extract()
        table = map(lambda x: x.replace(":","").replace("  "," ").title().strip(), table)
        i = 0
        status = 'field' #the other is value
        dic = {}
        while True:
            if i >= len(table)-1 or len(table) < 1:
                break
            if status == 'field':
                dic[table[i].lower()] = table[i+1]
                status = statusSwitch(status)
            else:
                i += 1
                status = statusSwitch(status)
                continue
            i += 1
        return dic

    def getBuildingAreas(self):
        """ Obtain the living areas, gross areas in each component for this property or parcel """
        def isEmptyCell(x):
            x = x.strip()
            if len(x) <= 1:
                return True
            else:
                return False
        def cleancelldata(xlist):
            if xlist == []:
                return "ERROR"
            x = map(lambda x: x.replace("  "," ").strip(), xlist)[0]
            if isEmptyCell(x):
                return ""
            else:
                return x

        bodypath = '//*[@id="MainContent_ctl01_grdSub"]/ \
                    tbody/tr[contains(@class,"RowStyle") or contains(@class,"FooterStyle")]'
        body_xpath = '//*[@id="MainContent_ctl01_grdSub"]/tbody/'
        #p = Selector(text=self.content).xpath('//*[@id="MainContent_ctl01_grdSub"]/tbody/tr[5]/td[1]/text()')
        nrows = len(Selector(text=self.content).xpath(bodypath).extract())
        lastrow_ind = False

        ## create the dictionary for the table lisitng buidling sub-areas (sq ft)
        dic = {}
        for i in range(2,nrows+2):
            firstcol = body_xpath + ("/tr[%s]/td[1]" %str(i)) + "/text()"
            firstcol_value = Selector(text=self.content).xpath(firstcol).extract()
            firstcol_value = cleancelldata(firstcol_value)

            secondcol = body_xpath + ("/tr[%s]/td[2]" %str(i)) + "/text()"
            secondcol_value = Selector(text=self.content).xpath(secondcol).extract()
            secondcol_value = cleancelldata(secondcol_value)

            thirdcol = body_xpath + ("/tr[%s]/td[3]" %str(i)) + "/text()"
            thirdcol_value = Selector(text=self.content).xpath(thirdcol).extract()
            thirdcol_value = cleancelldata(thirdcol_value)

            forthcol = body_xpath + ("/tr[%s]/td[4]" %str(i)) + "/text()"
            forthcol_value = Selector(text=self.content).xpath(forthcol).extract()
            forthcol_value = cleancelldata(forthcol_value)

            if firstcol_value == 'ERROR' or secondcol_value == 'ERROR' \
                    or thirdcol_value == "ERROR" or forthcol_value == "ERROR":
                break
            elif firstcol_value == "" or secondcol_value =="":
                lastrow_ind = True
            else:
                lastrow_ind = False
            if not(lastrow_ind):
                dic[secondcol_value+" ("+firstcol_value+")_GrossArea"] = thirdcol_value
                dic[secondcol_value+" ("+firstcol_value+")_LivingArea"] = forthcol_value
            else:
                dic["GrossArea"] = thirdcol_value
                dic["LivingArea"] = forthcol_value
        if len(dic.keys()) == 0:
            print("No Building Gross and Living Areas are available for %s" % self.getLocation())
        return dic

