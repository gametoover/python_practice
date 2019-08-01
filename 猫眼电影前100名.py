import time
import pandas as pd
import numpy as np
import requests
import re
import json
from requests.exceptions import RequestException

def get_one_page(url):
    try:
        headers = {'User_Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        respons = requests.get(url,headers = headers)
        if respons.status_code == 200:
            return respons.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('<i class="board-index board-index-\d+">(\d+)</i>.*?<img data-src="(.*?)" alt="(.*?)" class="board-img" />',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2].strip()
        }

def write_to_file(content):
    with open(r"C:\Users\xh-32\Desktop\tst.txt",'a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')

def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)
