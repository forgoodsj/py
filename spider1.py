#!/user/bin/env python
#coding=utf-8
import urllib.request
from urllib.error import URLError, HTTPError
import re
import chardet
import urllib.parse
import time
import urllib.robotparser
import datetime

def download(url, user_agent='wswp',proxy=None,num_retries=2):
    print('Downloading:' ,url)
    headers = {'User-agent':user_agent}
    request = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener()
    if proxy:
        #代理的处理
        proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))
    try:
        html = urllib.request.urlopen(request).read()
        encode_type = chardet.detect(html)
        html = html.decode(encode_type['encoding'])
    except HTTPError as e:
        print('Download error:',e.reason)
        html = None

        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code <600:
                #返回5XX错误时，代表服务器错误，这时候重新尝试
                return download(url, num_retries-1)

    return html

def crawl_sitemap(url): #通过robots.txt中的,xml来获取整站网页
    sitemap = download(url)
    # print(sitemap)
    #提取网站链接
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    #下载链接
    for link in links:
        html = download(link)
        pass

def link_crawler(seed_url,link_regex,robots_url):
    #通过初试链接和正则来爬网页上的所有链接，并且记录在网站池中，备用
    crawl_queue = [seed_url]
    #记住已经抓去过的链接
    seen = set(crawl_queue)
    # 检查地址是否被robots.txt的限制
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    user_agent = 'GoodCrawler'
    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch(user_agent, url):
            html = download(url)
            for link in get_links(html):
                # print(link)
                time.sleep(0.05)
                if re.match(link_regex, link):
                    #转换为绝对地址
                    link = urllib.parse.urljoin(seed_url,link)
                    #去重,加入已浏览队列
                    if link not in seen:
                        seen.add(link)
                        crawl_queue.append(link)
        else:
            print('Blocked by robots.txt',url)

def get_links(html):
    #返回html中的所有链接
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    #webpage_regex = re.compile('<a href="(.*?)">', re.IGNORECASE)
    return webpage_regex.findall(html)

class Throttle:
    #在下载中增加延迟
    #Throttle lei
    def __init__(self,delay):
        self.delay = delay
        self.domains = {}

    def wait(self,url):
        domain = urllib.parse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                #domain近期已经进入过，需要睡眠
                time.sleep(sleep_secs)
        #更新最近访问时间
        self.domains[domain] = datetime.datetime.now()

# url = 'http://httpstat.us/500'
# crawl_url='http://example.webscraping.com/sitemap.xml'
# crawl_url2='http://rss.eastmoney.com/sitemaps/stock_sitemap.xml'
# crawl_sitemap(crawl_url)
robots_url = 'http://example.webscraping.com/robots.txt'
seed_url = 'http://example.webscraping.com'
link_regex = '/places/default/(index|view)/'
link_crawler(seed_url,link_regex,robots_url)
