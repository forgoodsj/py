#!/user/bin/env python
#coding=utf-8
import urllib.request
import csv
import json

url = 'http://61.129.248.208/OpenAPI3.0/InnerAPI/Trade/GetFundAndCompanyCode'
request = urllib.request.Request(url)
html = urllib.request.urlopen(request).read()
# print(html)
# print(html[8:-62])
html1 = json.loads(html)
# print(html1)
writer = csv.writer(open('fund.csv','w'))
for f in html1['Data']:
    print(f['FCODE'],f['JJGSID'])
    writer.writerow([f['FCODE'],f['JJGSID']])



