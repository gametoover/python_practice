import requests
from urllib.parse import urlencode
import re
import time
import os
from multiprocessing.pool import Pool


def get_page(offset):
    params = {'cid': 36,
          'start':offset,
          'count': 30,

        }
    headers = {'cookie':'Hm_lvt_6e8dac14399b608f633394093523542e=1560477908; UM_distinctid=16b53bf3cf262c-0f13187cdfd513-3c644d0e-1fa400-16b53bf3cf3804; Hm_lvt_ea4269d8a00e95fdb9ee61e3041a8f98=1564969084,1565261448,1565261595; Hm_lpvt_ea4269d8a00e95fdb9ee61e3041a8f98=1565261595',
               'referer':'http://lab.mkblog.cn/wallpaper/',
               'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
               'x-requested-with':'XMLHttpRequest',
               'host':'lab.mkblog.cn'}
    base_url = 'http://lab.mkblog.cn/wallpaper/api.php?'
    url = base_url + urlencode(params)
    try:
        response = requests.get(url = url,headers = headers)
        if response.status_code == 200:
            return response.json(),url
    except requests.ConnectionError:
        return None


def parse_page(json):
    if json.get('data'):
        data =  json.get('data')
        for item in data:
            data_dict = {}
            data_dict['utag'] = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]','',str(item.get('utag'))).strip()
            data_dict['url_thumb'] = item.get('url_thumb')
            yield data_dict

def save_img(data_dict):
    path = r"E:\pyspider"
    if not os.path.exists(path):
        os.mkdir(path)
    for url_thumb in data_dict:
        img_path = path + '\\' +  str(url_thumb.get('utag')) + '.jpg'
        url = url_thumb.get('url_thumb')
        try:
            response = requests.get(url)
            if response.status_code == 200:
                response = response.content
                with open(img_path, 'wb') as f:
                    f.write(response)
                print('{}下载完毕'.format(url_thumb.get('utag')))
        except requests.ConnectionError:
            pass




def main(offset):
    json,url = get_page(offset)
    data_dict = parse_page(json)
    print(url)
    save_img(data_dict)


GROUP_START = 0
GROUP_END = 7

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 30 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()

    # for offset in [i * 30 for i in range(1,10)]:
    #     main(offset)
    #     time.sleep(1)

