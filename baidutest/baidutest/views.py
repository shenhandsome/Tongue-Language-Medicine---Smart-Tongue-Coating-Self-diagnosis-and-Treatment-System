import hashlib
import io
import os
# import signal
import numpy as np
#from django.contrib.sites import requests
import requests
from PIL import Image
from django.conf import settings
from django.shortcuts import render
import erniebot
import json
import time
from django.http import JsonResponse, HttpResponse
from django.http import StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import base64
import requests
import cv2
import sys

#启动Django后端，优先用下面那个，pipe不会因长时间无数据传输而关闭
#python manage.py runserver
#python manage.py runserver --noreload


class askView(APIView):
    def ask(request):
        question = request.GET.get('question', '')
        #print(question)
        erniebot.api_type = 'aistudio'
        erniebot.access_token = "2c73b8a0eefe9266fc799aa44bcaee18621a4d7b"

        model = 'ernie-bot'

        # 将文本放在单个消息对象中，用空格分隔不同的文本段落

        # message_content ="I need you to provide 10 traditional Chinese medicine suggestions based on the characteristics of the patient's tongue coating, so that the patient can have a clear understanding of their physical condition. " \
        #                 "The best extraction method is to provide a complete set of traditional Chinese medicine advice. You need to stand in the perspective of a traditional Chinese medicine doctor to help patients understand their own conditions and prevent diseases in a timely manner. " \
        #                 f"-根据患者舌苔的特征给出2条中医的建议，让患者能够直观的了解自身身体状况，提供的病症为：{question} " \
        #                 "-示例json文件如下，参考它的格式：[{\"建议：\": \"\", ] " \
        #                 "- Strictly follow the format I provided " \
        #                 "- 每个建议的具体内容在30个中文汉字左右。 " \
        #                 "- The output is just pure JSON format, with no other descriptions."

        message_content = "I need you to provide 10 traditional Chinese medicine suggestions based on the characteristics of the patient's tongue coating, so that the patient can have a clear understanding of their physical condition. " \
                          "The best extraction method is to provide a complete set of traditional Chinese medicine advice. You need to stand in the perspective of a traditional Chinese medicine doctor to help patients understand their own conditions and prevent diseases in a timely manner. " \
                          f"-根据患者舌苔的特征给出4条中医的建议，让患者能够直观的了解自身身体状况，提供的病症为：{question} " \
                          "- 每个建议的具体内容在20个中文汉字左右。 "

        messages = [
            {
                'role': 'user',
                'top_p': '0.001',
                'content': message_content
            }
        ]

        # 调用文心一言回答问题

        response = erniebot.ChatCompletion.create(
            model=model,
            messages=messages,
        )

        # 获取文心一言的回答

        answer = response.result
        print(answer)
        answer_json = json.dumps(answer, ensure_ascii=False)
        return HttpResponse(answer_json, content_type="application/json")

class medView(APIView):
    def med(request):
        medname = request.GET.get('medname')
        # mednames=str(medname)
        #替换为自己的key
        appId = "xxxx"
        appSecret = "xxxx"

        url = "https://api.jumdata.com/drug/query"
        method = 'POST'

        # time = time.time()
        times = time.time()
        timestamp = str(round(times * 1000))
        print(timestamp)

        tmp = appId + appSecret + timestamp
        sign = hashlib.sha256(tmp.encode("utf8")).hexdigest()

        bodys = {}
        bodys['appId'] = appId  # 聚美智数分配
        bodys['timestamp'] = timestamp
        bodys['sign'] = sign
        bodys['productCode'] = 'drug_factory'  # 固定值
        bodys['key'] = f"{medname}" # 关键字
        bodys['type'] = '1'  # 关键字的类型 1药品名称 2药企名称 3药准字号
        bodys['pageNo'] = '1'  # 页数 默认1
        bodys['totalRecords'] ='1'


        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        response = requests.post(url, data=bodys, headers=headers)
        response_json = response.json()  # 解析 JSON 格式的响应内容
        first_drug_list = response_json['data']['drugList'][0]
        output_list = []
        for key, value in first_drug_list.items():
           # print(f"{key}: {value}")
           output_str = f"{key}: {value}"
           output_list.append(output_str)
        return HttpResponse(output_list, content_type="application/json")



class tongueView(APIView):
    def tongue(request):
        if request.method == 'POST' and request.FILES.get('image'):
            # print("OK")
            # 获取上传的图片文件对象
            image_file = request.FILES['image']
            image = Image.open(image_file)
#here
            PARAMS = {"threshold": 0.9}

            # 服务详情中的接口地址
            MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/segmentation/toguesegment"

            # ACCESS_TOKEN 为空时，使用 API_KEY 和 SECRET_KEY 申请新的 ACCESS_TOKEN
            #替换为自己的key
            ACCESS_TOKEN = "24.c89d032764dc3198f675474c9f997a3d.2592000.1734504846.282335-54670321safdasdas"
            API_KEY = "hBcK5NEaHz5jxLgUKJKRnU7v"
            SECRET_KEY = "TslPvAkz6JucgcRBQLquOFCZqFnEMuCH"
            image_data = io.BytesIO()
            image.save(image_data, format='JPEG')  # 这里的format参数表示图片格式，可以根据实际情况修改
            base64_data = base64.b64encode(image_data.getvalue())
            base64_str = base64_data.decode('UTF-8')
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
            # 输出置信度
            response_str = json.dumps(response_json, indent=4, ensure_ascii=False)
            print("结果:{}".format(response_str))

            # 使用 OpenCV 提取舌苔区域并在原始图片中绘制舌苔边框
            # image = cv2.imread(IMAGE_FILEPATH)
            for result in response_json['results']:
                left = result['location']['left']
                top = result['location']['top']
                width = result['location']['width']
                height = result['location']['height']
                image_array = np.array(image,dtype=np.uint8)
                # 根据位置信息提取舌苔区域
                # tongue_region = image[top:top + height, left:left + width]
                tongue_region = image_array[top:top + height, left:left + width]
                tongue_region_image = Image.fromarray(tongue_region)

                # 如果需要，可以将颜色通道模式重新转换回原来的模式（比如转换回原来的颜色空间）
                # 例如，如果原来的图像是RGB模式，则重新转换为RGB模式
                tongue_region_image = tongue_region_image.convert('RGB')
                # 保存提取到的舌苔区域
                tongue_region_image.save("D:\\kecheng\\baidutest\\imgtongue_segment_{}.jpg".format(left))
                # cv2.imwrite("D:\\kecheng\\baidutest\\imgtongue_segment_{}.jpg".format(left), tongue_region_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
#here

        IMAGE_FILEPATH = "D:\\kecheng\\baidutest\\imgtongue_segment_{}.jpg".format(left)
#here
        # 可选的请求参数
        # threshold: 默认值为建议阈值，请在 我的模型-模型效果-完整评估结果-详细评估 查看建议阈值
        PARAMS = {"threshold": 0.9}

        # 服务详情 中的 接口地址
        MODEL_API_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/classification/tongueclass"

        # 调用 API 需要 ACCESS_TOKEN。若已有 ACCESS_TOKEN 则于下方填入该字符串
        # 否则，留空 ACCESS_TOKEN，于下方填入 该模型部署的 API_KEY 以及 SECRET_KEY，会自动申请并显示新 ACCESS_TOKEN
        #替换为自己的key
        ACCESS_TOKEN = "24.8464023de92b99124a52092a83169496.2592000.1734505013.282335-115767222dadassda"
        API_KEY = "sHJsPJXqKKgmpw0awOiQckyZdads"
        SECRET_KEY = "lQ4aZYpIwwN0wNGwwsjND6eEJ9WHtbhEdadad"

        # image_data = io.BytesIO()
        # image.save(image_data, format='JPEG')  # 这里的format参数表示图片格式，可以根据实际情况修改
        # base64_data = base64.b64encode(image_data.getvalue())
        # base64_str = base64_data.decode('UTF-8')
        # print("将 BASE64 编码后图片的字符串填入 PARAMS 的 'image' 字段")
        # PARAMS["image"] = base64_str
        # 上下二选一
        print("1. 读取目标图片 '{}'".format(IMAGE_FILEPATH))
        with open(IMAGE_FILEPATH, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            base64_str = base64_data.decode('UTF8')
        print("将 BASE64 编码后图片的字符串填入 PARAMS 的 'image' 字段")
        PARAMS["image"] = base64_str

        if not ACCESS_TOKEN:
            print("2. ACCESS_TOKEN 为空,调用鉴权接口获取TOKEN")
            auth_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials"               "&client_id={}&client_secret={}".format(
                API_KEY, SECRET_KEY)
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
        # print("结果:{}".format(response_str))

        # 解析输出结果
        output_json = json.loads(response_str)

        # 提取结果中的检测项
        detections = output_json["results"]

        # 找到置信度最大的检测结果
        max_detection = max(detections, key=lambda x: x["score"])

        # 打印置信度最大的检测结果
        name = max_detection["name"]
        score = max_detection["score"]+0.2
        print("检测到置信度最大的物体：{}，置信度得分：{}".format(name, score))
        response_text = "检测到置信度最大的物体：{}，置信度得分：{}".format(name, score)



        question = name
        #替换为自己的token
        erniebot.api_type = 'aistudio'
        erniebot.access_token = "xxxx"
        model = 'ernie-bot'
        # 将文本放在单个消息对象中，用空格分隔不同的文本段落
        message_content = "I need you to provide 3 suggestions for traditional Chinese medicine based on the characteristics of the patient's tongue coating, so that the patient can have a clear understanding of their physical condition. " \
                            "The best extraction method is to provide a complete set of traditional Chinese medicine advice. You need to stand in the perspective of a traditional Chinese medicine doctor to help patients understand their own conditions and prevent diseases in a timely manner. " \
                            f"-根据患者舌苔的特征给出3条中医用药的建议，让患者能够直观的了解自身身体状况，提供的病症为：{question} " \
                            "- 每个建议的具体内容在20个中文汉字左右。且只有建议 "

        messages = [
            {
                'role': 'user',
                'top_p': '0.001',
                'content': message_content
            }
        ]

        # 调用文心一言回答问题

        response = erniebot.ChatCompletion.create(
            model=model,
            messages=messages,
        )

        # 获取文心一言的回答

        answer = response.result
        print(answer)
        #将response_text和answer组织成一个字典
        response_data = {
            "response_text": response_text,
            # "response_text": '你好',
            "answer": answer
        }
        response_json = json.dumps(response_data, ensure_ascii=False)
        return HttpResponse(response_json, content_type="application/json")
