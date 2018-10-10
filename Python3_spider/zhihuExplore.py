#!/user/bin/env python
#coding=utf-8

import requests
from pyquery import PyQuery as pq

url = 'https://www.zhihu.com/explore'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}
html = requests.get(url,headers=headers).text
doc =pq(html)
items = doc('.explore-tab .feed-item').items() #遍历
for item in items:
    question = item.find('h2').text()
    author = item.find('.author-link-line').text()
    answer = pq(item.find('.content').html()).text()#.html获取html文本,包含加粗换行等
    print(pq(item.find('.content').html()))
    file = open('explore.txt','a',encoding='utf-8')
    file.write('\n'.join([question,author,answer]))
    file.write('\n' + '=' *50 +'\n')
    file.close()