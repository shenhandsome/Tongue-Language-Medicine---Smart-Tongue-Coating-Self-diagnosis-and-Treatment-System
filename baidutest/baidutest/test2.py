import json
import base64
import requests
import cv2

# 目标图片的本地文件路径，支持jpg/png/bmp格式
IMAGE_FILEPATH = r"D:\kecheng\baidutest\baidutest\static\23.jpg"

# 可选的请求参数
# threshold: 默认值为建议阈值，请在 我的模型-模型效果-完整评估结果-详细评估 查看建议阈值
PARAMS = {"threshold": 0.9}

# 服务详情中的接口地址
MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/segmentation/toguesegment"
###替换为自己的key
ACCESS_TOKEN = "24.c89d032764dc3198f675474c9f997a3d.2592000.1734504846.282335-5467032199999"
API_KEY = "hBcK5NEaHz5jxLgUKJKRnU7v"
SECRET_KEY = "TslPvAkz6JucgcRBQLquOFCZqFnEMuCH"

# 读取目标图片并进行 base64 编码
print("1. 读取目标图片 '{}'".format(IMAGE_FILEPATH))
with open(IMAGE_FILEPATH, 'rb') as f:
    base64_data = base64.b64encode(f.read())
    base64_str = base64_data.decode('UTF8')
print("将 BASE64 编码后图片的字符串填入 PARAMS 的 'image' 字段")
PARAMS["image"] = base64_str

# 若 ACCESS_TOKEN 为空，则申请新的 ACCESS_TOKEN
if not ACCESS_TOKEN:
    print("2. ACCESS_TOKEN 为空，调用鉴权接口获取 TOKEN")
    auth_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials" \
               "&client_id={}&client_secret={}".format(API_KEY, SECRET_KEY)
    auth_resp = requests.get(auth_url)
    auth_resp_json = auth_resp.json()
    ACCESS_TOKEN = auth_resp_json["access_token"]
    print("新 ACCESS_TOKEN: {}".format(ACCESS_TOKEN))
else:
    print("2. 使用已有 ACCESS_TOKEN")

# 向模型接口发送请求
print("3. 向模型接口 '{}' 发送请求".format(MODEL_API_URL))
request_url = "{}?access_token={}".format(MODEL_API_URL, ACCESS_TOKEN)
response = requests.post(url=request_url, json=PARAMS)
response_json = response.json()
#输出置信度
response_str = json.dumps(response_json, indent=4, ensure_ascii=False)
print("结果:{}".format(response_str))

# 使用 OpenCV 提取舌苔区域并在原始图片中绘制舌苔边框
# image = cv2.imread(IMAGE_FILEPATH)
# for result in response_json['results']:
#     left = result['location']['left']
#     top = result['location']['top']
#     width = result['location']['width']
#     height = result['location']['height']
#
#     # 根据位置信息提取舌苔区域
#     tongue_region = image[top:top+height, left:left+width]
#
#     # 保存提取到的舌苔区域
#     cv2.imwrite("tongue_segment_{}.jpg".format(left), tongue_region)
#
#     # 在原始图片上绘制舌苔区域的边框
#     cv2.rectangle(image, (left, top), (left+width, top+height), (0, 255, 0), 2)
#
# # 显示绘制了舌苔边框的图片
# cv2.imshow("Tongue Segmentation", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
