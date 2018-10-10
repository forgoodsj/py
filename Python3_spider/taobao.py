#!/user/bin/env python
#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote
from pyquery import PyQuery as pq

browser = webdriver.Firefox(executable_path="E:\python\geckodriver")
wait = WebDriverWait(browser, 100)#等待页面加载成功不然抛出异常
KeyWord = 'iPad'

def index_page(page):
    '''
    :param page: 页码
    :return:
    '''

    try:
        url = 'https://s.taobao.com/search?q=' + quote(KeyWord)
        browser.get(url)

        input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input'))
            )
        input_page = input.get_attribute('value')
        print(input_page)
        if page != input_page:  # 如果page不等于input,则跳转
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit'))
            )
            input.clear()
            input.send_keys(page)
            submit.click()

        #等待页面模块加载完成
        #利用当前高亮的页码是否为输入的页码数来判断是否跳转成功，若未跳转成功，则等待
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page))
        )
        print('span OK')
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemList .items .item'))
        )
        print('正在爬取第', page, '页')
        get_products()
    except TimeoutException:
        #index_page(page)
        print('GG')

def get_products():
    '''
    提取商品数据
    '''
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('data-src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text(),
        }
        print(product)


index_page(2)

