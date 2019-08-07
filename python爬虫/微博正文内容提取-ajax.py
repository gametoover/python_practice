from lxml import etree
from bs4 import BeautifulSoup
import requests
from pyquery import PyQuery as pq
from urllib.parse import urlencode

base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {'Host':'m.weibo.cn',
           'Referer':'https://m.weibo.cn/u/2830678474',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
           'X-Requested-With':'XMLHttpRequest'}
def get_page(page):
    parms = {'type':'uid',
             'value':'2830678474',
             'containerid':'1076032830678474',
             'page':page}
    url = base_url + urlencode(parms)
    try:
        response = requests.get(url=url,headers = headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('error',e.args)

def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = pq(item.get('text')).text().strip().replace('\n','')
            weibo['attitudes_count'] = item.get('attitudes_count')
            yield weibo

if __name__ == '__main__':
    json = get_page(2)
    result = parse_page(json)
    for i in result:
        print(i)
