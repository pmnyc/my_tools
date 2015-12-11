
# coding: utf-8


import pprint
import fiona
import pickle

addresses=[]
with fiona.open('gridpoly.shp') as src:
    #add range to index src
    for tt in src:
        tmp=tt['properties']
        addresses.append(str(tmp['Y_MIN'])+','+str(tmp['Y_MAX'])+','+str(tmp['X_MIN'])+','+str(tmp['X_MAX']))
        pprint.pprint(addresses)

type(addresses)
#address= 'http://www.trulia.com/for_sale/Worcester,MA/18_zm/'+address+'_xy/map_v'
#pprint.pprint(address)


import requests
proxies = {
  "http": "http://nmpc\myuser:temppwd((@192.168.85.13:8080",
  "https": "http://nmpc\myuser:temppwd((@192.168.85.13:8080",
}


linked=[]
for address in addresses:
    adr='http://www.trulia.com/for_sale/Worcester,MA/18_zm/'+address+'_xy/map_v'  
    r = requests.get(adr) # or add proxies=proxies if proxy is needed
    try:
        ind0=r.text.index('results:')
        txtp=r.text[ind0:]
        ind1=txtp.index('};');#print ind1
        tp= txtp[:ind1].replace('results:','')+'}'
        tps=filter(lambda x: x.startswith('"pdpURL":'),tp.split(','))
        for tpsu in tps:
            linked.append(tpsu.replace('"pdpURL":','').replace('"','').replace('\\',''))
            print linked[-1]
    except Exception as ex:
       pass
        #rx=requests.get('http://www.trulia.com/'+tps[0].replace('"pdpURL":','').replace('"','').replace('\\',''),proxies=proxies)
tset=set(map(tuple,linked))
pickle.dump(tset,open('links.p',"wb"))
#pickle.load( open( "links.p", "rb" ) )

