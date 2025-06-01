import json

import requests
import time
import hashlib
###替换为自己的api
appId = "po4aUNWv7sgs63od" 
appSecret = "e9d087f4dd4ab6b0e73f1a5495effb79"

url = "https://api.jumdata.com/drug/query"
method = 'POST'

time = time.time()
timestamp = str(round(time * 1000))
print (timestamp)

tmp = appId + appSecret + timestamp
sign = hashlib.sha256(tmp.encode("utf8")).hexdigest()

bodys = {}
bodys['appId'] = appId # 聚美智数分配
bodys['timestamp'] = timestamp
bodys['sign'] = sign
bodys['productCode']='drug_factory' # 固定值
bodys['key'] = '布洛芬混悬滴剂' # 关键字
bodys['type'] = '1' # 关键字的类型 1药品名称 2药企名称 3药准字号
bodys['pageNo'] = '1' # 页数 默认1

headers = {
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

response = requests.post(url, data = bodys, headers = headers)
response_json = response.json()  # 解析 JSON 格式的响应内容
first_drug_list = response_json['data']['drugList'][0]

for key, value in first_drug_list.items():
    print(f"{key}: {value}")