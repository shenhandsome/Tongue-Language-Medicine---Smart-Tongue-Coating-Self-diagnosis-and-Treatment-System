import requests
import json

def main():
    # 替换成你的 API Key 和 Secret Key
    # client_id = "sHJsPJXqKKgmpw0awOiQckyZ"  # 例如 'abcd1234'
    # client_secret = "lQ4aZYpIwwN0wNGwwsjND6eEJ9WHtbhE"  # 例如 'xyz9876'
    client_id = "xxx"  # 例如 'abcd1234'
    client_secret = "xxx"  # 例如 'xyz9876'

    # 拼接 URL
    url = f"https://aip.baidubce.com/oauth/2.0/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"
    
    # 不需要 payload，这个接口是 GET 请求
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # 发送请求并获取响应
    response = requests.post(url, headers=headers)
    
    # 打印获取到的 access_token
    print(response.text)

if __name__ == '__main__':
    main()
