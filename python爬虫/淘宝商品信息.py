import requests
import re
from pyquery import PyQuery as pq
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
KEYWORD = 'iPAD'

def index_page(page):
    print('正在爬取{}'.format(page))
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url=url)
        if page > 1:
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager div.form > input')))
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span'),str(page)))
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.m-itemlist div.items .item')))
        print('爬取第{}成功'.format(page))
        print('正在解析中。。。')
        html = browser.page_source
        doc = pq(html)
        items = doc('.m-itemlist div.items .item').items()
        for item in items:
            product = {'title':item.find('.pic-box-inner img').attr('alt'),
                       'data_src':item.find('.pic-box-inner img').attr('data-src'),
                       'product_link':item.find('.pic-box-inner a').attr('href'),
                       'price':item.find('.price.g_price.g_price-highlight').text(),
                       'paid_count':re.search('(\d+).*?',item.find('.deal-cnt').text(),re.S).group(1) }
            print(product)

    except TimeoutException:
        index_page(page)

def get_page():
    html = browser.page_source
    doc = pq(html)



if __name__ == '__main__':
    for i in range(1,10):
        index_page(i)
    browser.close()





# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from pyquery import PyQuery as pq
# from urllib.parse import quote



# # chrome_options = webdriver.ChromeOptions()
# # chrome_options.add_argument('--headless')
# # browser = webdriver.Chrome(chrome_options=chrome_options)
# browser = webdriver.Chrome()
#
# wait = WebDriverWait(browser, 10)
#
# KEYWORD = 'ipad'
#
# def index_page(page):
#     """
#     抓取索引页
#     :param page: 页码
#     """
#     print('正在爬取第', page, '页')
#     try:
#         url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
#         browser.get(url)
#         # if page > 1:
#         #     input = wait.until(
#         #         EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
#         #     submit = wait.until(
#         #         EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
#         #     input.clear()
#         #     input.send_keys(page)
#         #     submit.click()
#         wait.until(
#             EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
#         print('爬取成功')
#
#     except TimeoutException:
#         index_page(page)
#
#
#
#
#
# if __name__ == '__main__':
#     index_page(1)
#
#































