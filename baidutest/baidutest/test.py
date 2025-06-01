import erniebot                                 #引入文心api包
erniebot.api_type = 'aistudio'                  #定义使用的令牌的aistudio平台的
erniebot.access_token = "xxxx"            #引入自己的令牌:https://aistudio.baidu.com/usercenter/token
model = 'ernie-bot'                             #定义使用的模型是ernie-bot
message_content = "I need you to provide 10 traditional Chinese medicine suggestions based on the characteristics of the patient's tongue coating, so that the patient can have a clear understanding of their physical condition. " \
                  "The best extraction method is to provide a complete set of traditional Chinese medicine advice. You need to stand in the perspective of a traditional Chinese medicine doctor to help patients understand their own conditions and prevent diseases in a timely manner. " \
                  f"-根据患者舌苔的特征给出2条中医的建议，让患者能够直观的了解自身身体状况，提供的病症为：舌色偏红，苔色偏黄，无裂纹，无齿痕 " \
                  "- 每个建议的具体内容在30个中文汉字左右。 " \
                  "- The output is just pure JSON format, with no other descriptions."            #传给文心的文本
messages = [                                    #将文本和其他参数封装成消息，便于传给文心
    {
        'role': 'user',
        'top_p': '0.001',
        'content': message_content              #传输的文本
    }
]
response = erniebot.ChatCompletion.create(      # 调用文心一言回答问题，下方是相关参数
    model=model,
    messages=messages,
)
answer = response.result                        #将回答的文本传给answer变量
print(answer)                                   #输出查看