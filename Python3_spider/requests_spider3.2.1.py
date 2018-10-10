#!/user/bin/env python
#coding=utf-8

import requests
import re
from requests.auth import HTTPBasicAuth

# r = requests.get('https://baidu.com/')
# print(type(r))
# print(r.status_code)
# print(type(r.text))
# print(r.text)
# print(r.cookies)
#
# data = {
#     'age': '22',
#     'name': 'germey'
# }
#
# r = requests.get('http://httpbin.org/get',params = data)
#
# print(r.text)
#
# 爬取知乎发现页所有问题
# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
#
# }
# r = requests.get("https://www.zhihu.com/explore",headers=headers)
# print(r.text)
# pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)#re.S 它表示“.”（不包含外侧双引号，下同）的作用扩展到整个字符串，包括“\n”。
# titles = re.findall(pattern,r.text)
# print(titles)
#
#
# 抓取文件并且保存
# r = requests.get("https://github.com/favicon.ico")
# with open('favicon.ico','wb') as f:
#     f.write(r.content)


# 文件上传
# files = {'file':open('favicon.ico','rb')}
# r = requests.post("http://httpbin.org/post", files=files)
# print(r.text)


# 会话维持，通过session,可以做到模拟同一个会话不用担心cookies
# s = requests.Session()
# s.get('http://httpbin.org/cookies/set/number/18')
# r = s.get('http://httpbin.org/cookies')
# print(r.text)


# 身份认证
# r = requests.get('http://localhost:5000',auth=('username','password'))
# print(r.status_code)

# 正则几个要点
# 贪婪与非贪婪  .*为贪婪匹配，尽可能匹配多的  .*?非贪婪，尽可能匹配少的，如果在末尾，可能一个都不匹配
# 修饰符 result = re.match(......, re.S) re.S让.*?可以匹配换行符！！！很重要！！！
# match是从开头匹配的，如果开头就不匹配，就直接None,可用serach代替