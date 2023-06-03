import os

from ..models import *
from django import template

register = template.Library()

# 获取主机数量
@register.simple_tag
def Get_Host_Nums():
    return HostInfo.objects.filter(status=1).count()

@register.simple_tag
def Get_Dangerous_Image(terminal_number):
    if(terminal_number==None or terminal_number==''):
        terminal_number = '1223'
    # 定义图片所在的目录
    directory = "static/runData/waringData/"+terminal_number+"/danger/"
    if(not os.path.exists(directory)):
        return "https://img1.baidu.com/it/u=4030662401,269078702&fm=253&fmt=auto&app=120&f=JPEG?w=1080&h=675"

    # 获取目录中所有的文件
    all_files = os.listdir(directory)

    # 找到文件名最大的文件
    latest_file = max(all_files)
    if (latest_file == None or latest_file == ''):
        return "https://img1.baidu.com/it/u=4030662401,269078702&fm=253&fmt=auto&app=120&f=JPEG?w=1080&h=675"
    # 打印最新文件的文件名
    latest_file_path = os.path.join(directory, latest_file)

    print("最新的文件是：", latest_file_path)
    # 通过最新文件路径读取文件内容
    return latest_file_path

@register.simple_tag
def Get_Distance_Image(terminal_number):
    if(terminal_number==None or terminal_number==''):
        terminal_number = '1223'
    # 定义图片所在的目录
    directory = "static/runData/waringData/"+terminal_number+"/distance/"
    if(not os.path.exists(directory)):
        return "https://img1.baidu.com/it/u=4030662401,269078702&fm=253&fmt=auto&app=120&f=JPEG?w=1080&h=675"

    # 获取目录中所有的文件
    all_files = os.listdir(directory)

    # 找到文件名最大的文件
    latest_file = max(all_files)
    if (latest_file == None or latest_file == ''):
        return "https://img1.baidu.com/it/u=4030662401,269078702&fm=253&fmt=auto&app=120&f=JPEG?w=1080&h=675"
    # 打印最新文件的文件名
    latest_file_path = os.path.join(directory, latest_file)

    print("最新的文件是：", latest_file_path)
    # 通过最新文件路径读取文件内容
    return latest_file_path

@register.simple_tag
def Get_Fatigue_Image(terminal_number):
    if(terminal_number==None or terminal_number==''):
        terminal_number = '1223'
    # 定义图片所在的目录
    directory = "static/runData/waringData/"+terminal_number+"/fatigue/"

    if(not os.path.exists(directory)):
        return "https://img1.baidu.com/it/u=4030662401,269078702&fm=253&fmt=auto&app=120&f=JPEG?w=1080&h=675"

    # 获取目录中所有的文件
    all_files = os.listdir(directory)

    # 找到文件名最大的文件
    latest_file = max(all_files)
    if (latest_file == None or latest_file == ''):
        return "https://img1.baidu.com/it/u=4030662401,269078702&fm=253&fmt=auto&app=120&f=JPEG?w=1080&h=675"
    # 打印最新文件的文件名
    latest_file_path = os.path.join(directory, latest_file)

    print("最新的文件是：", latest_file_path)
    # 通过最新文件路径读取文件内容
    return latest_file_path


@register.simple_tag
def Get_Face_Image(terminal_number):
    if(terminal_number==None or terminal_number==''):
        terminal_number = '1223'
    # 定义图片所在的目录
    directory = "static/runData/waringData/"+terminal_number+"/face/"
    if(not os.path.exists(directory)):
        return "https://img1.baidu.com/it/u=4030662401,269078702&fm=253&fmt=auto&app=120&f=JPEG?w=1080&h=675"

    # 获取目录中所有的文件
    all_files = os.listdir(directory)

    # 找到文件名最大的文件
    latest_file = max(all_files)
    if (latest_file == None or latest_file == ''):
        return "https://img1.baidu.com/it/u=4030662401,269078702&fm=253&fmt=auto&app=120&f=JPEG?w=1080&h=675"
    # 打印最新文件的文件名
    latest_file_path = os.path.join(directory, latest_file)

    print("最新的文件是：", latest_file_path)
    # 通过最新文件路径读取文件内容
    return latest_file_path