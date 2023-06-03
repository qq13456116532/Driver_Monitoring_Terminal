######################################
# Django 模块
######################################
import base64
import os
import urllib
from io import BytesIO

import jwt
from PIL import Image
from django.contrib.sites import requests
from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

######################################
# 第三方模块
######################################
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

######################################
# 系统模块
######################################
import json
import datetime, time

######################################
# 自建模块
######################################
from utils.login_check import LoginStatusCheck
from .forms import *
from .models import *
from opms.settings import SERVER_URL
from users.models import UserProfile




######################################
# 发送警告消息
######################################
class SendWarningMessageView(View):
    @csrf_exempt
    def post(self, request):
        try:
            user_msg = "上传图片成功"
            data = json.loads(request.body)
            subject = data.get('subject', '')
            if subject == '1':
                subject1 = '前车碰撞报警'
                user_msg = subject1 + "的图片上传了，URL是"+data.get('distance', '')
            if subject == '2':
                subject1 = '危险驾驶报警'
                user_msg = subject1 + "的图片上传了，URL是"+data.get('danger', '')
            if subject == '3':
                subject1 = '疲劳驾驶报警'
                user_msg = subject1 + "的图片上传了，URL是"+data.get('fatigue', '')
            if subject == '4':
                subject1 = '驾驶员身份不匹配报警'
                user_msg = subject1 + "的图片上传了，URL是"+data.get('face', '')
            ms_type = 3
            user_msg = user_msg.replace('%%%%%', ';')
            terminal_number = data.get('terminal_number', '')
            # 保存消息
            message_info = MessageInfo()
            message_info.ms_type = ms_type
            message_info.subject = subject
            message_info.content = user_msg
            message_info.add_time = datetime.datetime.now()
            message_info.update_time = datetime.datetime.now()
            message_info.send_user_id = 1
            message_info.save()
            path =""
            try:
                imageUrl =''
                if(subject =='1'):
                    path = "distance"
                    imageUrl = data.get('distance', 'https://img0.baidu.com/it/u=1022428054,2283794670&fm=253&fmt=auto&app=138&f=JPEG?w=488&h=485')
                if(subject =='2'):
                    path    = "danger"
                    imageUrl = data.get('danger', 'https://img0.baidu.com/it/u=1022428054,2283794670&fm=253&fmt=auto&app=138&f=JPEG?w=488&h=485')
                if(subject =='3'):
                    path    = "fatigue"
                    imageUrl = data.get('fatigue', 'https://img0.baidu.com/it/u=1022428054,2283794670&fm=253&fmt=auto&app=138&f=JPEG?w=488&h=485')
                if(subject =='4'):
                    path    = "face"
                    imageUrl = data.get('face', 'https://img0.baidu.com/it/u=1022428054,2283794670&fm=253&fmt=auto&app=138&f=JPEG?w=488&h=485')
                # path 修改上传的路径
                file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) +".jpg"
                wholepath = "static/runData/waringData/"+terminal_number+"/" + path +"/"
                if not os.path.exists(wholepath):
                    os.makedirs(wholepath)
                # 发送HTTP请求获取图片数据
                cur = urllib.request.urlopen(imageUrl)
                response = cur.read()
                # 将响应数据以二进制形式保存
                image_data = response

                # 使用Pillow库解码图像数据
                image = Image.open(BytesIO(image_data))
                # 将图像保存到本地文件
                for root, dirs, files in os.walk("runData/"):
                    for file in files:
                        os.chmod(os.path.join(root, file), 0o777)
                    for dir in dirs:
                        os.chmod(os.path.join(root, dir), 0o777)
                with open(wholepath+ file_name, 'wb') as f:
                    f.write(image_data)
                img_url = SERVER_URL + '/' + wholepath+ file_name
                context = {
                    'status': 'success',
                    'img_url': img_url,
                }
                print(img_url)
                # return HttpResponse(json.dumps(context), content_type='application/json')
            except Exception as e:
                print(e)
                return HttpResponse('{"status":"failed", "msg":"上传失败！"}', content_type='application/json')
            # 添加接收用户
            users = UserProfile.objects.filter(status=1, is_active=True)
            user_id_list = users.values_list('id', flat=True)
            if len(user_id_list) == 0:
                for each in users:
                    user_id_list.append(each.id)

            for each_user_id in user_id_list:
                message_user_info = MessageUserInfo()
                message_user_info.message_id = message_info.id
                message_user_info.user_id = each_user_id
                message_user_info.is_star = False
                if each_user_id != request.user.id:
                    message_user_info.is_read = False
                else:
                    message_user_info.is_read = True
                message_user_info.status = 1
                message_user_info.save()
            return HttpResponse('{"status":"success", "msg":"发送成功！"}', content_type='application/json')
        except Exception as e:
            print(e)
            return HttpResponse('{"status":"failed", "msg":"发送失败！"}', content_type='application/json')


######################################
# 消息列表
######################################
class MessageListView(LoginStatusCheck, View):
    def get(self, request, web_tag):
        # 页面选择
        web_chose_left_1 = 'user_management'
        web_chose_left_2 = 'user_message'
        web_chose_middle = web_tag

        msgs = MessageUserInfo.objects.filter(user=request.user).filter(status=1)

        title = '收件箱'

        # 发件箱
        if web_tag == 'send_list':
            msgs = msgs.filter(message__send_user=request.user)
            title = '发件箱'

        # 未读信息
        if web_tag == 'unread_list':
            msgs = msgs.filter(is_read=False)
            title = '未读信息'

        # 星标信息
        if web_tag == 'star_list':
            msgs = msgs.filter(is_star=True)
            title = '星标信息'

        # 通知信息
        if web_tag == 'notify_list':
            msgs = msgs.filter(message__ms_type=1)
            title = '通知信息'

        # 搜索
        keyword = request.GET.get('keyword', '')
        if keyword != '':
            msgs = msgs.filter(Q(message__subject__icontains=keyword) | Q(message__content__icontains=keyword) | Q(
                message__send_user__chinese_name__icontains=keyword))

        # 归档
        year = request.GET.get("year", '')
        month = request.GET.get("month", '')

        if (year != '') and (month != ''):
            msgs = msgs.filter(message__add_time__year=int(year), message__add_time__month=int(month))
            web_chose_middle = str(year) + str(month)

        msgs = msgs.order_by('-message__update_time')

        msg_nums = msgs.count()

        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(msgs, 16, request=request)

        # 分页处理后的 QuerySet
        msgs = p.page(page)

        context = {
            'web_chose_left_1': web_chose_left_1,
            'web_chose_left_2': web_chose_left_2,
            'web_chose_middle': web_chose_middle,
            'msgs': msgs,
            'title': title,
            'keyword': keyword,
            'msg_nums': msg_nums,
        }

        return render(request, 'message/message/message_list.html', context=context)


######################################
# 消息详情
######################################
class MessageDetailView(LoginStatusCheck, View):
    def get(self, request, web_tag, msg_id):
        # 页面选择
        web_chose_left_1 = 'user_management'
        web_chose_left_2 = 'user_message'
        web_chose_middle = web_tag

        # 主消息
        msg_start = MessageInfo.objects.get(id=int(msg_id))

        # 回复
        msg_replay = MessageReplayInfo.objects.filter(message_id=int(msg_id))

        # 标记为已读
        user_msg = MessageUserInfo.objects.get(message=msg_start, user=request.user)
        if not user_msg.is_read:
            user_msg.is_read = True
            user_msg.save()

        if not msg_replay:
            msg_replay = ''

        rec_users = MessageUserInfo.objects.filter(message_id=msg_start.id).exclude(user_id=request.user.id)

        context = {
            'web_chose_left_1': web_chose_left_1,
            'web_chose_left_2': web_chose_left_2,
            'web_chose_middle': web_chose_middle,
            'msg_start': msg_start,
            'msg_replay': msg_replay,
            'rec_users': rec_users,
        }

        return render(request, 'message/message/message_detail.html', context=context)


######################################
# 发送消息
######################################
class SendMessageView(LoginStatusCheck, View):
    def post(self, request):
        try:
            subject = request.POST.get('subject', '')
            if subject == '':
                subject = '无标题'

            user_id_list = []
            if request.POST.getlist('rec_users'):
                for each_user in request.POST.getlist('rec_users'):
                    user_id_list.append(int(each_user))

            # 获取消息类型
            ms_type = 3

            if len(user_id_list) == 1:
                ms_type = 2

            # 消息内容
            user_msg = request.POST.get('user_msg', '')

            user_msg = user_msg.replace('%%%%%', ';')

            # 保存消息
            message_info = MessageInfo()
            message_info.send_user = request.user
            message_info.ms_type = ms_type
            message_info.subject = subject
            message_info.content = user_msg
            message_info.save()

            # 添加接收用户
            users = UserProfile.objects.filter(status=1, is_active=True)

            if len(user_id_list) == 0:
                for each in users:
                    user_id_list.append(each.id)
            else:
                user_id_list.append(request.user.id)

            for each_user_id in user_id_list:
                message_user_info = MessageUserInfo()
                message_user_info.message_id = message_info.id
                message_user_info.user_id = each_user_id
                message_user_info.is_star = False
                if each_user_id != request.user.id:
                    message_user_info.is_read = False
                else:
                    message_user_info.is_read = True
                message_user_info.status = 1
                message_user_info.save()
            return HttpResponse('{"status":"success", "msg":"发送成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"failed", "msg":"发送失败！"}', content_type='application/json')


######################################
# 上传图片
######################################
class UploadMessagImageView(LoginStatusCheck, View):
    def post(self, request):
        try:
            # path 修改上传的路径
            path = "media/message/upload/" + time.strftime("%Y%m%d%H%M%S", time.localtime())
            f = request.FILES["file"]
            file_name = path + "_" + f.name
            des_origin_f = open(file_name, "wb+")
            # 直接遍历类文件类型就可以生成迭代器了
            for chunk in f:
                des_origin_f.write(chunk)
            des_origin_f.close()
            img_url = SERVER_URL + '/' + file_name
            context = {
                'status': 'success',
                'img_url': img_url,
            }
            print(img_url)
            return HttpResponse(json.dumps(context), content_type='application/json')
        except Exception as e:
            print(e)
            return HttpResponse('{"status":"failed", "msg":"上传失败！"}', content_type='application/json')


######################################
# 回复消息
######################################
class ReplayMessageView(LoginStatusCheck, View):
    def post(self, request):
        try:
            msg_id = request.POST.get('msg_id')

            # 消息内容
            user_msg = request.POST.get('user_msg', '')

            user_msg = user_msg.replace('%%%%%', ';')

            UserReplay = MessageReplayInfo()
            UserReplay.message_id = msg_id
            UserReplay.replay_user_id = request.user.id
            UserReplay.content = user_msg
            UserReplay.save()

            msg_user = MessageUserInfo.objects.filter(message_id=msg_id)
            if msg_user:
                for each in msg_user:
                    if each.user.id != request.user.id:
                        each.is_read = False
                        each.save()

            return HttpResponse('{"status":"success", "msg":"发送成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"failed", "msg":"发送失败！"}', content_type='application/json')


######################################
# 星标消息
######################################
class StarMessageView(LoginStatusCheck, View):
    def post(self, request):
        try:
            msg_id = int(request.POST.get('msg_id'))
            user_msg = MessageUserInfo.objects.get(message_id=msg_id, user_id=request.user.id)
            if user_msg.is_star:
                user_msg.is_star = False
            else:
                user_msg.is_star = True
            user_msg.save()
            return HttpResponse('{"status":"success", "msg":"星标成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"failed", "msg":"星标失败！"}', content_type='application/json')


######################################
# 标记已读
######################################
class AddMessageReadView(LoginStatusCheck, View):
    def post(self, request):
        try:
            check_list = request.POST.getlist("msg_check")
            if len(check_list):
                for each in check_list:
                    each_msg = MessageUserInfo.objects.get(message_id=int(each), user=request.user)
                    if not each_msg.is_read:
                        each_msg.is_read = True
                        each_msg.save()
            return HttpResponse('{"status":"success", "msg":"标记已读成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"failed", "msg":"标记已读失败！"}', content_type='application/json')


######################################
# 标记所有已读
######################################
class AddAllMessageReadView(LoginStatusCheck, View):
    def post(self, request):
        try:
            unread_msgs = MessageUserInfo.objects.filter(user=request.user, is_read=False)
            for each in unread_msgs:
                each.is_read = True
                each.save()
            return HttpResponse('{"status":"success", "msg":"标记已读成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"failed", "msg":"标记已读失败！"}', content_type='application/json')

