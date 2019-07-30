import pandas as pd
import numpy as np
from pathlib import Path
import json
import re
import os
import datetime
from sqlalchemy import create_engine


# 找到文件夹下所有的txt文本文档，将其放入list中
def find_file(path):
	file_list = []
	p = Path(path)
	for i in list(p.glob("**/*.txt")):
		file_list.append(i)
	return file_list


b = {'time': [],
	 # 'topic__': [],
	 'source': [],
	 # 'Xiao_User_Agent': [],
	 'Role': [],
	 'Real_Ip': [],
	 'User_Agent': [],
	 'room_id': [],
	 'payload':[]}




def file_parsing(file_list):
	for file in file_list:
		with open(file, "r+", encoding="utf-8-sig") as f:
			file_content = f.readlines()
			for i in file_content:
				dict_json = json.loads(i)
				b['time'].append(dict_json['__time__'])
				# b['__topic__'].append(dict_json['__topic__'])
				b['source'].append(dict_json['__source__'])
				content = dict_json['content']

				if re.findall("X-Role:\[(.*?)\]", content):
					b['Role'].append(re.findall("X-Role:\[(.*?)\]", content)[0])
				else:
					b['Role'].append(0)

				if re.findall("X-Real-Ip:\[(.*?)\]", dict_json['content']):
					b['Real_Ip'].append(re.findall("X-Real-Ip:\[(.*?)\]", content)[0])
				else:
					b['Real_Ip'].append(0)

				if re.findall("X-User-Agent:\[(.*?)\]", dict_json['content']):
					b['User_Agent'].append(re.findall("X-User-Agent:\[(.*?)\]", content)[0])
				else:
					b['User_Agent'].append(0)

				if re.findall("room_id=([0-9]{4})", dict_json['content']):
					b['room_id'].append(re.findall("room_id=([0-9]{4})", dict_json['content'])[0])
				else:
					b['room_id'].append(0)

				if re.findall('-Payload:\[(.*?)\]',dict_json['content']):
					b['payload'].append(re.findall('-Payload:\[(.*?)\]',dict_json['content'])[0])
				else:
					b['payload'].append(0)
	return b


# 剔除X_User_Agent为空的数据
data = pd.DataFrame(b)

def valid_data(dict_json):
	raw_data = pd.DataFrame(dict_json)
	raw_data = raw_data[(raw_data.User_Agent != 0) | (raw_data.room_id != 0)]
	raw_data['time'] = raw_data['time'].apply(
		lambda x: datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
	processed_data = pd.concat([data, raw_data])
	processed_data = processed_data.reset_index(drop=True)
	return processed_data


path_list = []
for i in range(0,5):
	path = r"F:\直播业务\{}".format(str(i))
	path_list.append(path)


def data_saved(processed_data):
	con = create_engine("mysql+pymysql://pangbin:D0423jkds2#dsj22@10.10.8.1:3906/bi_eduboss_xinghuo?charset=utf8")
	pd.io.sql.to_sql(processed_data, 'tmp_zb_log_data', con, schema='bi_eduboss_xinghuo', if_exists='append')
	con.dispose()
	return print("数据存储完毕")


def main():
    for path in path_list:
        if os.path.exists(path):
            print('即将开始获取{}内容'.format(path))
            file_list = find_file(path)
            print('{}获取文件完毕'.format(path))
            b = file_parsing(file_list)
            print('{}文件解析完毕'.format(path))
            processed_data = valid_data(b)
            print('{}数据已存储成DataFrame格式'.format(path))
            data_saved(processed_data)
            print("{}数据已存储至数据库".format(path))
	return processed_data

if __name__ == '__main__':
   main()




