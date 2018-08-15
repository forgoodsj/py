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
import lxml.html
import csv
import random

DEFAULT_AGENT = 'wswp'
DEFAULT_DELAY = 5
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 60

class Throttle:
    #在下载中增加延迟
    #Throttle 类
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

class Downloader:
    def __init__(self,delay=5,
                 user_agent='wswp',proxies=None,#代理
                 num_retries=1,cache=None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache

    def __call__(self,url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                #url不在缓存列表中
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] <= 600:
                    # 返回5XX错误时，代表服务器错误，这时候重新尝试
                    # 并且重新下载
                    result = None

        if result is None:
            #结果没有在缓存中时下载
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url,headers,proxy,self.num_retries)
            if self.cache:
                self.cache[url] = url
        return result['html']

    def download(url, user_agent='wswp', proxy=None, num_retries=2,data=None):
        print('Downloading:', url)
        headers = {'User-agent': user_agent}
        request = urllib.request.Request(url, headers=headers)
        opener = urllib.request.build_opener()
        if proxy:
            # 代理的处理
            proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            html = urllib.request.urlopen(request).read()
            encode_type = chardet.detect(html)
            html = html.decode(encode_type['encoding'])
        except HTTPError as e:
            print('Download error:', e.reason)
            html = ''
            if hasattr(e,'code'):
                code =e.code
                if num_retries > 0 and 500 <= e.code < 600:
                    # 返回5XX错误时，代表服务器错误，这时候重新尝试
                    return self._get(url,headers,proxy,num_retries-1,data)
            else:
                code = None

        return {'html':html,'code':code}


D = Downloader(delay = 5,user_agent = 'wswp', proxies = None,  # 代理
num_retries = 1, cache = None)

def crawl_sitemap(url): #通过robots.txt中的,xml来获取整站网页
    sitemap = D.download(url)
    # print(sitemap)
    #提取网站链接
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    #下载链接
    for link in links:
        html = D.download(link)
        pass

def link_crawler(seed_url,link_regex ,robots_url,delay=1, max_depth=2, scrape_callback = None,cache=None):
    #通过初试链接和正则来爬网页上的所有链接，并且记录在网站池中，备用
    crawl_queue = [seed_url]
    #记住已经抓去过的链接
    seen = {seed_url:0}
    #seen = set(crawl_queue)
    # 检查地址是否被robots.txt的限制
    num_urls = 0
    rp = urllib.robotparser.RobotFileParser()
    D = Downloader(delay=delay, user_agent='wswp', proxies=None,  # 代理
                   num_retries=1, cache=cache)
    throttle = Throttle(delay)
    rp.set_url(robots_url)
    rp.read()
    user_agent = 'GoodCrawler'
    #D =
    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch(user_agent, url):
            #增加延迟
            throttle.wait(url)
            html = D.download(url)
            links = []
            if scrape_callback:
                links.extend(scrape_callback(url,html) or [])

            #深度
            depth = seen[url]
            if depth != max_depth:
                if link_regex:
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))
                for link in get_links(html):
                    # print(link)

                    if re.match(link_regex, link):
                        #转换为绝对地址
                        link = urllib.parse.urljoin(seed_url,link)
                        #去重,加入已浏览队列
                        if link not in seen:
                            seen[link] = depth + 1
                            if same_domain(seed_url, link):
                                # success! add this new link to queue
                                crawl_queue.append(link)

        else:
            print('Blocked by robots.txt',url)


def get_links(html):
    #返回html中的所有链接
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    #webpage_regex = re.compile('<a href="(.*?)">', re.IGNORECASE)
    return webpage_regex.findall(html)



def same_domain(url1, url2):
        """Return True if both URL's belong to same domain
        """
        return urllib.parse.urlparse(url1).netloc == urllib.parse.urlparse(url2).netloc

class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv','w'))
        self.fields = ('places_area__row','places_population__row','places_iso__row','places_country__row',
          'places_country__row','places_capital__row','places_continent__row'
          , 'places_tld__row','places_currency_code__row','places_currency_name__row'
          , 'places_phone__row','places_postal_code_format__row','places_postal_code_regex__row'
          , 'places_languages__row','places_neighbours__row')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):

        if re.search('/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#%s > td.w2p_fw' % field)[0].text_content())
            self.writer.writerow(row)







# url = 'http://httpstat.us/500'
# crawl_url='http://example.webscraping.com/sitemap.xml'
# crawl_url2='http://rss.eastmoney.com/sitemaps/stock_sitemap.xml'
# crawl_sitemap(crawl_url)

robots_url = 'http://example.webscraping.com/robots.txt'
seed_url = 'http://example.webscraping.com'
link_regex = '/places/default/(index|view)/'


link_crawler(seed_url,link_regex,robots_url,max_depth=5, scrape_callback=ScrapeCallback())