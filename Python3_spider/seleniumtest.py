#!/user/bin/env python
#coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import time

"""
模拟打开浏览器，然后访问页面，留下源代码
"""




# browser = webdriver.Chrome(executable_path="C:\\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver")
browser = webdriver.Firefox(executable_path="E:\python\geckodriver")
# try:
#     browser.get('https://www.taobao.com')  #请求网址
#     input = browser.find_element_by_id('kw')
#     input.send_keys('Python')
#     input.send_keys(Keys.ENTER)
#     wait = WebDriverWait(browser, 10)
#     wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
#     print(browser.current_url)
#     print(browser.get_cookies())
#     print(browser.page_source)
# finally:
#     browser.close()


# browser.get('https://www.taobao.com')

# input_first = browser.find_element_by_id('q')#找到id为q的元素,只能找到第一个，即淘宝的输入框
# input_second = browser.find_element_by_css_selector('#q')
# input_third = browser.find_element_by_xpath('//*[@id="q"]')
# print(input_first,input_second,input_third)

# lis = browser.find_elements_by_css_selector('.service-bd li')#找多个节点，以list返回
# print(lis)

'''
节点交互
send_keys() 输入文字
clear() 清空文字
click() 点击
'''
# input = browser.find_element_by_id('q')
# input.send_keys('知网')
# # time.sleep(1)
# # input.clear()
# # input.send_keys('iPad')
# button = browser.find_element_by_class_name('btn-search')
# button.click()



url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
wait = WebDriverWait(browser, 10)
browser.get(url)
browser.switch_to.frame('iframeResult')
source = browser.find_elements_by_css_selector('#draggable')
source1 = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#draggable'))
)
target = browser.find_elements_by_css_selector('#droppable')
target1 = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#droppable'))
)
actions = ActionChains(browser)
actions.drag_and_drop(source1, target1)
actions.perform()


'''调用js'''
# browser.get('https://www.zhihu.com/explore')
# browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# browser.execute_script('alert("To Bottom')


'''获取属性'''
# browser.get('https://www.zhihu.com/explore')
# logo = browser.find_element_by_id('zh-top-link-logo')
# print(logo)
# print(logo.get_attribute('class'))
# browser.close()
