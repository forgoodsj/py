#!/user/bin/env python
#coding=utf-8

html ="""
<html><head><title> The Dormouse's story</title></head>
<body >
<p class="title"  name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href ="http://example.com/elsie" class= "sister" id ="linkl"><!-- Elsie --></a>,
<a href ="http://example.com/lacie" class ="sister" id ="link2"> Lacie</a>  and
<a href="http://example.com/tillie"  class ="sister" id ="link3"> Tillie</a>;
and they lived at the bottom of a well.</p>
<p class ="story">  ...  <Ip>
from  bs4 import BeautifulSoup
"""
from bs4 import BeautifulSoup
soup = BeautifulSoup(html,'lxml')
# print(soup.prettify())
print(soup.title.string)
print(soup.head)
print(soup.p)
print(soup.title.name) #获取节点名称
print(soup.p.attrs)#获取属性
print(soup.p.attrs['name'])#获取属性名称
print(soup.p['name']) #同上


