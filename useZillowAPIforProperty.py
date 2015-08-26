#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: pm

************************************
Zillow For all APIs
    Limit queries to 1,000 per day, per API. If you think you need more, Please request a higher call limit by filling out a request form

Sample Deep Search Path (the last zip code can be dropped):
    http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=X1-myzillowid&address=2114+Bigelow+Ave&citystatezip=Seattle%2C+WA+98109
Sample Deep Comparable Results (recent 5 results)
    http://www.zillow.com/webservice/GetDeepComps.htm?zws-id=X1-myzillowid&zpid=48749425&count=5
Sample Updated Property Details
    http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?zws-id=X1-myzillowid&zpid=48749425
************************************
Setup:
    1) Create a folder "config" in work direcotry, and get in this folder
    2) Create json file "settings.json", the sample setting is
        {
            "zws-id": "X1-ZWzcolpsamdfla",
            "zillow_account": "myemail@myemail.com"
        }
    3) Create json file "zillowAPI.json", its setting is
        {
            "deepsearch_link":"http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id={zwsid}&address={address}&citystatezip={citystate}",
            "deepcomps_link":"http://www.zillow.com/webservice/GetDeepComps.htm?zws-id={zwsid}&zpid={zpid}&count=5",
            "updatedproperty_link":"http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?zws-id={zwsid}&zpid={zpid}"
        }

************************************
Sample Usage:
>>> obj = deepsearch("2114 bigelow ave ", "Seattle ,    WA 98101 ")
>>> output_dict = obj.getFinalDict()
>>> obj.cleanup()

Individual file results are as follows
obj.deepsearch_dict; obj.updatedProperty_dict

"""

import os, copy, time
import json
import urllib2
import xmltodict
import fnmatch

class deepsearch(object):
    """ This is to obtain the info for calling Zillow API """
    def __init__(self, address, citystatezip):
        self.address_raw = address
        self.citystatezip = citystatezip
        self.clean_address_info = cleanAddress(address, citystatezip)
        self.city = self.clean_address_info["city"]
        self.state = self.clean_address_info["state"]
        self.address = self.clean_address_info["address"]
        ## This is to create the log folder if it does not exist##
        self.logfile = os.path.join(os.getcwd(),'log/log')
        self.errorlogfile = os.path.join(os.getcwd(),'log/error_log')
        createFolder("log")
        if not(os.path.isfile(self.logfile)):
            f= open(self.logfile, 'a')
            f.close()
        if not(os.path.isfile(self.errorlogfile)):
            f= open(self.errorlogfile, 'a')
            f.close()
        ## This is to create log info that will be written into log files ##
        self.loginfo = ""
        self.errorloginfo = ""

    # This is to obtail the zid that is specific to the parcel/address
    def downloadSetting(self):
        setting_dict = loadJson(os.path.join(os.getcwd(),'config/settings.json'))
        zillowapi_dict = loadJson(os.path.join(os.getcwd(),'config/zillowAPI.json'))
        self.zwsid = setting_dict['zws-id']
        self.deepsearchlink = zillowapi_dict['deepsearch_link']
        self.deepcomps_link = zillowapi_dict['deepcomps_link']
        self.updatedproperty_link = zillowapi_dict['updatedproperty_link']
        address = self.address
        city = self.city
        state = self.state
        self.address_city_state = address+" "+city+", "+state

    def downloadDeepSearch(self, download_folder="downloads"):
        self.downloadSetting()
        createFolder(download_folder)
        dplink = self.deepsearchlink
        zwsid = self.zwsid
        address = self.address
        city = self.city
        state = self.state
        citystate = city+"%2C "+state
        info = {"zwsid": str(zwsid), 
                "address":"+".join(address.split()),
                "citystate":"+".join(citystate.split())}
        self.deepsearchlink = dplink.format(**info)

        filename = address+city+state+"_deepsearch.xml"
        filename = filename.replace(" ","")
        newfile = os.path.join(os.getcwd(),download_folder,filename)
        downloadXML(self.deepsearchlink,newfile)
        self.loginfo = self.loginfo + "File "+filename+" was downloaded on "+timeStamp()+". \n"
        self.deepsearch_file = newfile
        if not(XMLexistsInd(newfile)):
            self.errorloginfo = self.errorloginfo+"File "+filename+" does not exist!! "+timeStamp()+" \n"
            self.deepsearch_file_error = True
        else:
            self.deepsearch_file_error = isXMLerror(newfile)

    def parseDeepsearch(self):
        self.downloadDeepSearch()
        if not(self.deepsearch_file_error):
            self.zpid = ''
            if self.deepsearch_file_error:
                self.deepsearch_dict = {}
            else:
                self.deepsearch_dict = parseDeepSearch(self.deepsearch_file)
                self.zpid = self.deepsearch_dict['zpid']
        else:
            raise Exception("Deep Search file download for "+self.address_city_state+" failed on "+timeStamp())

    ### Done with Deep Search File, now search for Deep Comparable file ###
    ## Deep Comparable Files are not very necessary for the purpose of ##
        ## of this project because it contains the same info as the ##
        ## deep search file except it contains more comparable properties ##
        ## info ##
    def downloadDeepComparable(self, download_folder="downloads"):
        try:
            if len(self.zpid) > 1 or self.zpid == '':
                pass
        except:
            self.parseDeepsearch()
        deepcomps_link = self.deepcomps_link
        address = self.address
        city = self.city
        state = self.state

        info = {"zwsid": str(self.zwsid), 
                "zpid":self.zpid}
        self.deepcomps_link = deepcomps_link.format(**info)
        filename = address+city+state+"_deepcomps.xml"
        filename = filename.replace(" ","")
        newfile = os.path.join(os.getcwd(),download_folder,filename)
        downloadXML(self.deepcomps_link,newfile)

        self.loginfo = self.loginfo + "File "+filename+" was downloaded on "+timeStamp()+". \n"
        self.deepcomps_file = newfile
        if not(XMLexistsInd(newfile)):
            self.errorloginfo = self.errorloginfo+"File "+filename+" does not exist!! "+timeStamp()+" \n"
            self.deepcomps_file_error = True
        else:
            self.deepcomps_file_error = isXMLerror(newfile)

    ### Now search for Updated Property file ###
    def downloadUpdatedProperty(self, download_folder="downloads"):
        try:
            if len(self.zpid) > 1 or self.zpid == '':
                pass
        except:
            self.parseDeepsearch()
        updatedproperty_link = self.updatedproperty_link
        address = self.address
        city = self.city
        state = self.state

        info = {"zwsid": str(self.zwsid), 
                "zpid":self.zpid}
        self.updatedproperty_link = updatedproperty_link.format(**info)
        filename = address+city+state+"_updated.xml"
        filename = filename.replace(" ","")
        newfile = os.path.join(os.getcwd(),download_folder,filename)
        downloadXML(self.updatedproperty_link,newfile)

        self.loginfo = self.loginfo + "File "+filename+" was downloaded on "+timeStamp()+". \n"
        self.upadtedproperty_file = newfile
        if not(XMLexistsInd(newfile)):
            self.errorloginfo = self.errorloginfo+"File "+filename+" does not exist!! "+timeStamp()+"\n"
            self.updatedproperty_file_error = True
        else:
            self.updatedproperty_file_error = isXMLerror(newfile)

    def parseUpdatedProperty(self):
        self.downloadUpdatedProperty()
        if not(self.updatedproperty_file_error):
            self.updatedProperty_dict = parseUpdateProperty(self.upadtedproperty_file)
        else:
            self.errorloginfo = self.errorloginfo+"Updated Property file download for "+self.address_city_state+" failed on "+timeStamp()+"\n"

    ##########   Post Process #########
    ## This is for cleaning up the downloaded files, and write log files ##
    def cleanup(self):
        files = [self.deepsearch_file, self.upadtedproperty_file]
        clean(files)
        with open(self.logfile, "a") as text_file:
            text_file.write(self.loginfo + "\n")
        text_file.close()
        if len(self.errorloginfo) > 1:
            with open(self.errorlogfile, "a") as text_file:
                text_file.write(self.errorloginfo + "\n")
            text_file.close()

    ## This is for combining the deepsearch xml info and updated property info ##
    def getFinalDict(self):
        try:
            x = self.updatedProperty_dict
        except AttributeError:
            self.parseUpdatedProperty()
        try:
            x = combineDicts(self.deepsearch_dict,self.updatedProperty_dict)
        except:
            self.loginfo += "Updated property info for "+self.address_city_state+" does not exist. "+timeStamp()
            x = self.deepsearch_dict
        return x

## end of class deepsearch ##


def loadJson(filename):
    json_data=open(filename,'r')
    data = json.load(json_data)
    json_data.close()
    return data

def createFolder(myfolder):
    # sample
    # myfolder = 'downloads'
    myfolder = os.path.join(os.getcwd(),myfolder)
    if not(os.path.isdir(myfolder)):
        os.makedirs(myfolder)
    else:
        pass

def downloadXML(url,newfile):
    # newfile = '~/myfile/2114BiglowAveSeattleWA.xml'
    s = urllib2.urlopen(url)
    contents = s.read()
    file = open(newfile, 'w')
    file.write(contents)
    file.close()

def XMLexistsInd(xmlfile):
    try:
        with open(xmlfile) as fd:
            xmlobj = xmltodict.parse(fd.read())
        del xmlobj
        boolean_ans = True
    except Exception:
        boolean_ans = False
    return boolean_ans

## Check if the xml file returned is a failed one ##
def isXMLerror(xmlfile):
    if XMLexistsInd(xmlfile):
        with open(xmlfile) as fd:
            xmlobj = xmltodict.parse(fd.read())
        try:
            errorcode = xmlobj[xmlobj.keys()[0]]['message']['code']
            error_ind = (str(errorcode) != '0')
        except Exception:
            error_ind = False
    else:
        print("File "+xmlfile+" does not exist!!")
        error_ind = True
    return error_ind

## parse the deep search xml file ##
def parseDeepSearch(xmlfile):
    # sample input
    # xmlfile = '2114BigelowAveSeattleWA_deepsearch.xml'
    with open(xmlfile) as fd:
        xmlobj = xmltodict.parse(fd.read())
    def getinSingleDict(dic):
        if len(dic.keys()) == 1:
            return dic[dic.keys()[0]]
        else:
            return dic
    xmlinfo = getinSingleDict(getinSingleDict(getinSingleDict(xmlobj)['response']))
    for i in range(10):
        if len(xmlinfo.keys())==1:
            xmlinfo = getinSingleDict(xmlinfo)
        else:
            break
    finaldict = dict(copy.copy(xmlinfo))
    mykeys = copy.copy(finaldict.keys())
    ## remove keys with more layers ##
    for key in mykeys:
        if ('dict' in str(type(finaldict[key]))) or \
            'OrderedDict' in str(type(finaldict[key])):
            del finaldict[key]
        else:
            continue
    try:
        finaldict['lastSoldPrice'] = '$' + xmlinfo['lastSoldPrice']['#text']
    except KeyError:
        pass
    ## add address info ##
    try:
        for key in xmlinfo['address'].keys():
            if key in finaldict.keys():
                continue
            else:
                finaldict[key] = xmlinfo['address'][key]
    except:
        pass
    ## add zestmate info ##
    try:
        x = xmlinfo['zestimate']
        finaldict['zestimate_last-updated'] = x['last-updated']
    except:
        pass
    try:
        finaldict['zestimate_amount'] = '$' + x['amount']['#text']
    except:
        pass
    ## add localRestate info ##
    try:
        finaldict['neighborhood'] = xmlinfo['localRealEstate']['region']['@name']
    except:
        pass
    return finaldict

## parse the deep comparable xml files ##
def parseDeepComps(xmlfile):
    # sample input
    # xmlfile = '2114BigelowAveSeattleWA_deepcomps.xml'
    with open(xmlfile) as fd:
        xmlobj = xmltodict.parse(fd.read())
    # define a program to get in dictionary if there is only one key
    def getindictwithonekey(xmlobj):
        if len(xmlobj.keys()) == 1:
            return xmlobj[xmlobj.keys()[0]]
        else:
            return xmlobj
    ## end ##
    xmlinfo = getindictwithonekey(xmlobj)['response']
    xmlinfo = getindictwithonekey(xmlinfo)['principal']
    return xmlinfo

## parse the updated property xml file ##
def parseUpdateProperty(xmlfile):
    # sample input
    # xmlfile = '2114BigelowAveSeattleWA_updated.xml'
    with open(xmlfile) as fd:
        xmlobj = xmltodict.parse(fd.read())
    # define a program to get in dictionary if there is only one key
    def getindictwithonekey(xmlobj):
        if len(xmlobj.keys()) == 1:
            return xmlobj[xmlobj.keys()[0]]
        else:
            return xmlobj
    ## end ##
    xmlinfo = getindictwithonekey(xmlobj)['response']
    # The following function is load new keys and info into the outputdic #    
    def loadinsideDic(dic,outputdic):
        for key in dic.keys():
            if key in outputdic.keys():
                continue
            else:
                outputdic[key] = dic[key]
        return outputdic
    # end #
    # The following program is to return boolean for whether an obj is dictioanry #
        # or not #
    def isDict(x):
        typestr = str(type(x)).lower()
        if ('dict' in typestr)  or ('ordereddict' in typestr):
            return True
        else:
            return False
    # end #
    finaloutput = {}
    finaloutput = loadinsideDic(xmlinfo['editedFacts'],finaloutput)
    othersignlekeys = filter(lambda t: not(isDict(xmlinfo[t])),xmlinfo.keys())
    for key in othersignlekeys:
        if key in finaloutput.keys():
            continue
        else:
            finaloutput[key] = xmlinfo[key]
    ## add some links ##
    try:
        finaloutput['images_links'] = xmlinfo['images']['image']['url']
    except:
        pass
    try:    
        finaloutput['homeDetails_links'] = xmlinfo['links']['homeDetails']
    except:
        pass
    try:    
        finaloutput['homeInfo_links'] = xmlinfo['links']['homeInfo']
    except:
        pass
    try:
        finaloutput['photoGallery_links'] = xmlinfo['links']['photoGallery']
    except:
        pass
    return finaloutput

## Clean up the list of files ##
def clean(files):
    if len(files) < 1:
        pass
    elif 'str' in str(type(files)):
        try:
            os.remove(files)
        except:
            pass
    else:
        for f in files:
            try:
                os.remove(f)
            except:
                pass
## end ##

## The following combines two dictionaries into one dictionary ##
def combineDicts(firstdict,seconddict):
    a = copy.copy(firstdict)
    b = copy.copy(seconddict)
    if 'dict' not in str(type(a)).lower():
        raise Exception('The 1st Dictionary in combineDicts function is not a dictionary')
    else:
        pass
    if 'dict' not in str(type(b)).lower():
        raise Exception('The 2nd Dictionary in combineDicts function is not a dictionary')
    else:
        pass
    for key in b.keys():
        if key in a.keys():
            continue
        else:
            a[key] = b[key]
    return a

## Get current time stamp ##
def timeStamp():
    """returns a formatted current time/date"""
    #sample: 'Tue 18 Aug 2015 11:13:41 AM'
    #str(time.strftime("%a %d %b %Y %I:%M:%S %p"))
    return str(time.strftime("%b %d %Y %I:%M:%S %p"))

#################################
## The following part is for parsing address
#################################
"""
This program is to clean up the "semi-structured" address

Remark:
    1. State provided must be a two-character string, not the full name of the state

Sample Usage:
>>> cleanAddress(address="2114 bigelow ave ", citystatezip="Seattle ,    WA 98101-1101 ")

You'd expect to see
    {'address': '2114 Bigelow Ave',
     'city': 'Seattle',
     'state': 'WA',
     'zip': '98101-1101'}
"""

def stripExtraSpace(x):
    """ This is to strip blanks from both ends and strip double spaces """
    return " ".join(x.strip().split())

def removeCharInList(string,comparelist):
    """ This is to remove characters in string that are in comparelist"""
    strs = copy.copy(string)
    for i in range(len(comparelist)):
        strs = strs.replace(comparelist[i],'')
    return strs

def list_numbers():
    listofNumbers = map(lambda x: str(x), range(10))
    listofNumbers_2 = [x+'-'+y for x in listofNumbers for y in listofNumbers]
    return (listofNumbers, listofNumbers_2)

def list_states():
    l1 = ["AL","AK","AZ","AR","CA","CO","CT", \
            "DE","FL","GA","HI","ID","IL","IN", \
            "IA","KS","KY","LA","ME","MD","MA", \
            "MI","MN","MS","MO","MT","NE","NV", \
            "NH","NJ","NM","NY","NC","ND","OH", \
            "OK","OR","PA","RI","SC","SD","TN", \
            "TX","UT","VT","VA","WA","WV","WI","WY"]
    l2 = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", \
            "Delaware", "Florida",  "Georgia",  "Hawaii",   "Idaho", "Illinois",  \
            "Indiana",  "Iowa",  "Kansas",   "Kentucky",  "Louisiana", "Maine", \
            "Maryland",  "Massachusetts", "Michigan",  "Minnesota", "Mississippi", \
            "Missouri",  "Montana",  "Nebraska",  "Nevada",   "New Hampshire", \
            "New Jersey",   "New Mexico",   "New York",  "North Carolina",   \
            "North Dakota",  "Ohio",  "Oklahoma",  "Oregon",   "Pennsylvania",  \
            "Rhode Island",  "South Carolina",   "South Dakota",  "Tennessee", \
            "Texas", "Utah",  "Vermont",  "Virginia",  "Washington",   \
            "West Virginia", "Wisconsin", "Wyoming",  "District of Columbia"]
    lists = l1
    return lists

def findState(x):
    # x = " los anageles, cA"
    allstates = list_states()
    state = ""
    x2 = copy.copy(x)
    x2 = " " + x2 + " "
    for i in range(len(allstates)):
        if fnmatch.fnmatch(x2,"* "+allstates[i]+" *"):
            state = allstates[i]
            break
    if state == "":
        raise Exception("No State info is given in address!!")
    else:
        return state

def formalizeWords(x):
    # for example
    # x = "los Angeles city"
    def capital1st(x0):
        letters = "abcdefghijklmnopqrstuvwxyz"
        if len(x0) >0:
            if x0[0] in letters:
                x0 = x0[0].upper() + x0[1:]
        return x0
    output = x
    if len(x) >0:
        words = x.split()
        output = map(capital1st,words)
        output = " ".join(output)
    return output

def cityStateZip(citystatezip):
    """ This is to obtain city, state and zip info 
        if the string of city, state and zipcode is given """
    citystate_2 = citystatezip.replace(","," , ").replace("."," ").replace("+"," ")
    citystate_2 = stripExtraSpace(citystate_2)
    citystate_2 = citystate_2.replace(" , ",", ")
    citystate_3 = removeCharInList(removeCharInList(citystate_2,list_numbers()[1]),list_numbers()[0])
    citystate_3 = stripExtraSpace(citystate_3.replace(",",""))
    citystate_4 = removeCharInList(citystate_3,map(lambda t: " "+t,list_states()))
    city = removeCharInList(citystate_4,map(lambda t: " "+t.lower(),list_states()))
    city = stripExtraSpace(city)
    state = findState(citystate_3)
    # now extract zipcode info
    zipinfo = citystate_2.replace(city,"").upper().replace(state.upper(),"").replace(",","")
    zipcode = stripExtraSpace(zipinfo)
    city = formalizeWords(city)
    out = {"city": city, "state":state, "zip":zipcode}
    return out

def getaddress(address):
    """ This is to concatenante the address using + without space """
    address_2 = address.replace(","," ").replace("."," ").replace("+"," ")
    address_2 = stripExtraSpace(address_2)
    address_3 = formalizeWords(address_2)
    return address_3

def cleanAddress(address, citystatezip):
    return{"address":getaddress(address),"city":cityStateZip(citystatezip)["city"],
            "state":cityStateZip(citystatezip)["state"],
            "zip":cityStateZip(citystatezip)["zip"]}
