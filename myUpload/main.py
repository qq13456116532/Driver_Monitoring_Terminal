# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
import requests
import json
import base64
from PIL import Image
import glob
import os


# url = 'http://127.0.0.1:2230'  # Web应用程序的地址
# data = {'key1': 'value1', 'key2': 'value2'}  # 要发送的数据，使用字典形式
#
# response = requests.post(url, json=data)  # 发送POST请求并传递数据
#
# if response.status_code == 200:  # 响应状态码为200表示请求成功
#     print(response.json())  # 打印响应内容，使用JSON解析响应体
# else:
#     print('请求失败')
#
#

# 获取图像的base64
def get_image_base64(path):
    with open(path, 'rb') as f:
        # Read the entire file
        data = f.read()

        # Convert the binary data to Base64
        b64 = base64.b64encode(data).decode()

    return b64

# 客户端   --str-> username,password   服务器
# 客户端   <--str-- token   服务器
# str -> dict
# 客户端   token,img--str-->   服务器
# 客户端   <--str--{mg:"..."}   服务器

# 上传图片，获得服务器返回的url
def get_image_url(base_url, path, img_token):
    upload_url = base_url + 'upload_file'
    files = {"file": open(path, "rb")}
    # file = get_image_base64(path)
    # files = {"file": file}
    headers = {'token': token}
    r = requests.post(upload_url, files=files, verify=False, headers=headers)
    if r.status_code == 200:
        print(r.text)
        res = json.loads(r.text)
        if res.get('code') == 200:
            print(res.get('msg'))
            img_url = res.get('data').get('url')
            print("图片上传："+img_url)
            return img_url
        else:
            print("aa"+res.get('msg'))
            return ""
    else:
        print("上传图片:" + r.status_code)
        return ""

# url = 'http://8.130.28.89:8000/api/'
url = 'http://localhost:8000/api/'
login_url = url + 'login'
login_data = {
    'username': 'adminyhm',
    'password': 'adminmm'
}
token = ""
# 把字典转成字符串
response = requests.post(login_url, data=json.dumps(login_data))
if response.status_code == 200:
    result = json.loads(response.text)
    if result.get('code') == 200:
        print(result.get('msg'))
        token = result.get('data').get('token')
        print("token:"+token)
    else:
        print("用户名密码不对")
else:
    print(response.status_code)

evt_data_url = url + 'send_event_data'

# 指定目录路径和通配符
dir_path = './images'
pattern = '*.jpg'

# 获取符合通配符的文件列表
file_list = glob.glob(os.path.join(dir_path, pattern))

# 遍历文件列表
for file_path in file_list:
    # 进行相应处理
    print(file_path)

    picture_base64 = get_image_base64(file_path)
    picture_url = get_image_url(url, file_path, token)

    evt_data = {
        "data": {
            "location": {
                "longitude": "1",
                "latitude": "2"
            },
            "road": "3",
            "picture_url": picture_url,
            "picture_base64": picture_base64,
            "detail_type": "4",
            "remarks": "no",
        },
        "create_time": "5",
        "data_type": "1005", #1003是distance，1004是danger，1005是fatigue
        "id": "7" # 车辆终端的ID, 目前1or2or3,需要添加车辆终端并在汽车及终端绑定才能上传
    }
    headers = {'content-type': 'application/json', 'token': token}
    response = requests.post(evt_data_url, headers=headers, data=json.dumps(evt_data))
    if response.status_code == 200:
        result = json.loads(response.text)
        if result.get('code') == 200:
            print(result.get('msg'))
        else:
            print(result.get('msg'))
    else:
        print(response.status_code)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
