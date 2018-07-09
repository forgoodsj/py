#!/user/bin/env python
#coding=utf-8

import re
from bs4 import BeautifulSoup
import lxml.html
import time
import spider1
import csv

#FIELDS = ('places_area__row','population','iso','country','capital','continent','tld','currency_code','currency_name',
#          'phone','postal_code_format','postal_code_regex','languages','beighbours',)
FIELDS = ('places_area__row','places_population__row','places_iso__row','places_country__row',
          'places_country__row','places_capital__row','places_continent__row'
          , 'places_tld__row','places_currency_code__row','places_currency_name__row'
          , 'places_phone__row','places_postal_code_format__row','places_postal_code_regex__row'
          , 'places_languages__row','places_neighbours__row')


# def re_scraper(html):#执行1000次耗时 5.5s
#     results = {}
#     for field in FIELDS:
#         results[field] = re.search('<tr id= %s>.*?<td class="w2p_fw">(.*?)</td> %field' , html).groups()[0]
#     return results


def bs_scraper(html):#执行1000次耗时 42.84s
    soup = BeautifulSoup(html,'html.parser')
    results = {}
    for field in FIELDS:
        results[field] = soup.find('table').find('tr',
            id= field).find('td',
                class_='w2p_fw').text
    return results

def lxml_scraper(html):#执行1000次耗时 7.06s
    tree = lxml.html.fromstring(html)
    results = {}
    for field in FIELDS:
        results[field] = tree.cssselect('table > tr#%s > td.w2p_fw'%field )[0].text_content()
    return results


NUM_ITERATIONS = 1000
html = spider1.download('http://example.webscraping.com/places/default/view/United-Kingdom-239')

for name, scraper in [
                      # ('Regular expressions',re_scraper),
                      ('BeautifulSoup', bs_scraper),
                      ('Lxml', lxml_scraper),
                      ]:
    #记录当前时间
    start = time.time()
    for i in range(NUM_ITERATIONS):
        # if scraper == re_scraper:
        #     re.purge()
        # result = scraper(html)
        #检查结果是否为预期结果
        result = scraper(html)
        assert(result['places_area__row'] == '244,820 square kilometres')


    #记录结束时间
    end = time.time()
    print('%s: %.2f seconds' %(name, end-start))

def scrape_callback(url, html):
    if re.search('default/view/', url):
        tree = lxml.html.fromstring(html)
        row = [tree.cssselect('table > %s > td.w2p_fw' % field)[0].text_content() for field in FIELDS]
    print(url,row)

class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv','w'))
        self.fields = ('places_area__row','places_population__row','places_iso__row','places_country__row',
          'places_country__row','places_capital__row','places_continent__row'
          , 'places_tld__row','places_currency_code__row','places_currency_name__row'
          , 'places_phone__row','places_postal_code_format__row','places_postal_code_regex__row'
          , 'places_languages__row','places_neighbours__row')
        self.writer.writerow(self.fields[7:-5])

    def __call__(self, url, html):
        if re.search('default/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#{} > td.w2p_fw'.format(field))[0].text_content())
        self.writer.writerow(row)
