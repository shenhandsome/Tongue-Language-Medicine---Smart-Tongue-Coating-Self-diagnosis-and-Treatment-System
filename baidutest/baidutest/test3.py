
"""
EasyDL 物体检测 调用模型公有云API Python3实现
"""

import json
import base64
import requests
"""
使用 requests 库发送请求
使用 pip（或者 pip3）检查我的 python3 环境是否安装了该库，执行命令
  pip freeze | grep requests
若返回值为空，则安装该库
  pip install requests
"""


# 目标图片的 本地文件路径，支持jpg/png/bmp格式
#IMAGE_FILEPATH = r"D:\kecheng\baidutest\baidutest\static\23.jpg"
IMAGE_FILEPATH = r"D:\kecheng\baidutest\img\3bgO5fEmecRo712579f1e6af5b6329656625a30d2f75.jpg"
# 可选的请求参数
# threshold: 默认值为建议阈值，请在 我的模型-模型效果-完整评估结果-详细评估 查看建议阈值
PARAMS = {"threshold": 0.9}

# 服务详情 中的 接口地址
MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/classification/tongueclass"

# 调用 API 需要 ACCESS_TOKEN。若已有 ACCESS_TOKEN 则于下方填入该字符串
# 否则，留空 ACCESS_TOKEN，于下方填入 该模型部署的 API_KEY 以及 SECRET_KEY，会自动申请并显示新 ACCESS_TOKEN
#替换为自己的key
ACCESS_TOKEN = "24.8464023de92b99124a52092a83169496.2592000.1734505013.282335-115767222wijkl"
API_KEY = "sHJsPJXqKKgmpw0awOiQckyZ"
SECRET_KEY = "lQ4aZYpIwwN0wNGwwsjND6eEJ9WHtbhE"

print("1. 读取目标图片 '{}'".format(IMAGE_FILEPATH))
with open(IMAGE_FILEPATH, 'rb') as f:
    base64_data = base64.b64encode(f.read())
    base64_str = base64_data.decode('UTF8')
print("将 BASE64 编码后图片的字符串填入 PARAMS 的 'image' 字段")
PARAMS["image"] = base64_str


if not ACCESS_TOKEN:
    print("2. ACCESS_TOKEN 为空,调用鉴权接口获取TOKEN")
    auth_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials"               "&client_id={}&client_secret={}".format(API_KEY, SECRET_KEY)
    auth_resp = requests.get(auth_url)
    auth_resp_json = auth_resp.json()
    ACCESS_TOKEN = auth_resp_json["access_token"]
    print("新 ACCESS_TOKEN: {}".format(ACCESS_TOKEN))
else:
    print("2. 使用已有 ACCESS_TOKEN")


print("3. 向模型接口 'MODEL_API_URL' 发送请求")
request_url = "{}?access_token={}".format(MODEL_API_URL, ACCESS_TOKEN)
response = requests.post(url=request_url, json=PARAMS)
response_json = response.json()
response_str = json.dumps(response_json, indent=4, ensure_ascii=False)
print("结果:{}".format(response_str))

# 解析输出结果
output_json = json.loads(response_str)

# 提取结果中的检测项
detections = output_json["results"]

# 找到置信度最大的检测结果
max_detection = max(detections, key=lambda x: x["score"])

# 打印置信度最大的检测结果
name = max_detection["name"]
score = max_detection["score"]
print("检测到置信度最大的物体：{}，置信度得分：{}".format(name, score))
