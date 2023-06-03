import datetime
import os
import tempfile
import time
import urllib
from io import BytesIO
from urllib.parse import unquote
import os
import zipfile
from django.http import FileResponse
import xlwt
from django.contrib.sites import requests
from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.utils import timezone
from django.utils.baseconv import base64
from django.views import View
import base64
from pure_pagination import PageNotAnInteger, Paginator

from auto_terminal.models import AutoTerminalInfo
from driver.models import DriverInfo


class DeleteDriverView(View):
    def post(self, request):
        driver = DriverInfo.objects.get(id=int(request.POST.get('id')))
        driver.delete()
        return HttpResponse('{"status":"success", "msg":"删除成功！"}', content_type='application/json')


class AddDriverView(View):
    def post(self, request):
        print("看一下request： ", request.POST)
        di = DriverInfo()
        if (request.POST.get('gender') != ''):
            di.gender = request.POST.get('gender', di.gender)
        if (request.POST.get('name') != ''):
            di.name = request.POST.get('name', di.name)
        if (request.POST.get('age') != ''):
            di.age = request.POST.get('age', di.age)
        if (request.POST.get('driving_experience')):
            di.driving_experience = request.POST.get('driving_experience', di.driving_experience)
        if (request.POST.get('phone_number')):
            di.phone_number = request.POST.get('phone_number', di.phone_number)
        if (request.POST.get('email')):
            di.email = request.POST.get('email', di.email)
        if(request.POST.get('fileInput')):
            avatar = request.POST.get('fileInput')
            # 从base64编码的字符串中获取图片数据
            image_data = avatar.split(",")[1]

            # 解码图片数据
            decoded_image_data = base64.b64decode(image_data)
            # 获取当前的时间，并将其格式化为一个字符串
            current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            # 图片文件的路径
            image_file_path = os.path.join("static", "runData", f"Person_{current_time}.jpg")
            # 将图片数据写入文件
            with open(image_file_path, "wb") as image_file:
                image_file.write(decoded_image_data)
            di.photo = "../" + image_file_path

        di.fatigue_driving_count = 0
        di.dangerous_driving_count = 0
        di.update_time = datetime.datetime.now()
        di.front_collision_warning_count = 0
        di.rear_collision_warning_count = 0
        di.save()
        return HttpResponse('{"status":"success", "msg":"添加成功！"}',
                            content_type='application/json')


######################################
# 首页
######################################
class DriverListView(View):
    def get(self, request):
        # 页面选择
        web_chose_left_1 = 'driver'
        web_chose_left_2 = 'list'
        web_chose_middle = ''

        title = '驾驶员'
        # 搜索的条件
        start_time = request.GET.get("start_time", "")
        stop_time = request.GET.get("stop_time", "")
        driving_experience = request.GET.getlist("experience", "")
        name = request.GET.get("name", "")
        export_data = ""
        action = request.GET.get("action", "")
        drivers = DriverInfo.objects.all().order_by("id")
        drivers_experiences = drivers.values_list("driving_experience", flat=True)
        drivers_names = drivers.values_list("name", flat=True)
        if action != "":
            if (action == "search") or (action == "export_search"):
                if start_time != "":
                    drivers = drivers.filter(update_time__gte=start_time)
                if stop_time != "":
                    drivers = drivers.filter(update_time__lte=stop_time)
                if driving_experience != "":
                    drivers = drivers.filter(driving_experience__in=driving_experience)
                if name!= "":
                    drivers = drivers.filter(name=name)
            if action == "export_search":
                export_data = drivers
            if (action == "export_all"):
                export_data = drivers

            if (action == "export_search") or (action == "export_all"):
                if (action == "export_search" and start_time == '' and stop_time == '' and name == ''):
                    return HttpResponse('{"status":"failed", "msg":"没有选择条件！"}', content_type='application/json')

                # 创建目录
                dir_name = "static/runData/"
                # os.makedirs(dir_name, exist_ok=True)

                # 创建zip文件
                zip_file_path = dir_name + "driver.zip"
                zipf = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)

                # 创建 excel
                new_excel = xlwt.Workbook(encoding='utf-8')
                excel_page = new_excel.add_sheet(u'驾驶员')

                # 插入第一行标题
                excel_page.write(0, 0, u'id')
                excel_page.write(0, 1, u'姓名')
                excel_page.write(0, 2, u'性别')
                excel_page.write(0, 3, u'驾驶证编号')
                excel_page.write(0, 4, u'年龄')
                excel_page.write(0, 5, u'驾龄')
                excel_page.write(0, 6, u'手机号')
                excel_page.write(0, 7, u'邮箱')
                excel_page.write(0, 8, u'疲劳驾驶次数')
                excel_page.write(0, 9, u'危险驾驶次数')
                excel_page.write(0, 10, u'前车碰撞预警次数')
                excel_page.write(0, 11, u'更新时间')
                excel_page.write(0, 12, u'人脸识别对比照片')
                # 初始行
                excel_row = 1

                if (export_data != '') and export_data:
                    for each in export_data:
                        image_path = each.photo[3:]  # 你的图片路径
                        new_name = str(each.id) + ".jpg"  # 新的文件名
                        if os.path.exists(image_path):
                            zipf.write(image_path, arcname=new_name)
                            excel_page.write(excel_row, 12, str(each.id) + ".jpg")

                        id_excel = each.id
                        name_excel = each.name
                        gender_excel = each.gender
                        license_number_excel = each.license_number
                        age_excel = each.age
                        driving_experience_excel = each.driving_experience
                        phone_number_excel = each.phone_number
                        email_excel = each.email
                        fatigue_driving_count_excel = each.fatigue_driving_count
                        dangerous_driving_count_excel = each.dangerous_driving_count
                        front_collision_warning_count_excel = each.front_collision_warning_count
                        update_time_excel = each.update_time

                        # 定义时间格式
                        time_style = 'YYYY/MM/DD HH:mm'
                        style = xlwt.XFStyle()
                        style.num_format_str = time_style

                        # 写数据
                        excel_page.write(excel_row, 0, id_excel)
                        excel_page.write(excel_row, 1, name_excel)
                        excel_page.write(excel_row, 2, gender_excel)
                        excel_page.write(excel_row, 3, license_number_excel)
                        excel_page.write(excel_row, 4, age_excel)
                        excel_page.write(excel_row, 5, driving_experience_excel)
                        excel_page.write(excel_row, 6, phone_number_excel)
                        excel_page.write(excel_row, 7, email_excel)
                        excel_page.write(excel_row, 8, fatigue_driving_count_excel)
                        excel_page.write(excel_row, 9, dangerous_driving_count_excel)
                        excel_page.write(excel_row, 10, front_collision_warning_count_excel)
                        excel_page.write(excel_row, 11, update_time_excel, style)

                        # 行数加1
                        excel_row += 1

                    # 导出文件
                    time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
                    filename = '驾驶员_' + time_now + '.xls'
                    # 创建一个临时文件
                    temp_file = tempfile.NamedTemporaryFile(delete=False)

                    # 保存Excel文件到临时文件
                    new_excel.save(temp_file.name)

                    # 添加临时文件到zip文件
                    zipf.write(temp_file.name, arcname=filename)

                    # 关闭临时文件
                    temp_file.close()

                    # 删除临时文件
                    os.remove(temp_file.name)

                    # 关闭zip文件
                    zipf.close()

                    # 创建一个FileResponse对象，将zip文件发送给用户
                    response = FileResponse(open(zip_file_path, 'rb'))
                    response['Content-Type'] = 'application/zip'
                    response['Content-Disposition'] = 'attachment; filename={}'.format(os.path.basename(zip_file_path))

                    return response

                    # response = HttpResponse(content_type='application/vnd.ms-excel')
                    # response['Content-Disposition'] = 'attachment;filename={}'.format(
                    #     filename.encode('utf-8').decode("ISO-8859-1"))
                    # output = BytesIO()
                    # new_excel.save(output)
                    # output.seek(0)
                    # response.write(output.getvalue())
                    # return response

        # 过滤
        # carends = AutoTerminalInfo.objects.filter(belong=1).filter(is_public=True)
        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(drivers, 17, request=request)

        # 分页处理后的 QuerySet
        drivers = p.page(page)

        context = {
            'web_chose_left_1': web_chose_left_1,
            'web_chose_left_2': web_chose_left_2,
            'web_chose_middle': web_chose_middle,
            'title': title,
            'drivers': drivers,
            'drivers_experiences': drivers_experiences,
            'drivers_names': drivers_names
        }
        return render(request, 'driver/driverlist.html', context=context)


######################################
# 编辑
######################################
class EditDriverView(View):
    def post(self, request):
        print("看一下request： ", request.POST)
        try:
            id = request.POST.get('id', '')
            if id != '':
                pu = DriverInfo.objects.get(id=int(id))
                if (request.POST.get('name') != ''):
                    pu.name = request.POST.get('name')
                if (request.POST.get('gender') != ''):
                    pu.gender = request.POST.get('gender')
                if (request.POST.get('license_number') != ''):
                    pu.license_number = request.POST.get('license_number')
                if (request.POST.get('age') != ''):
                    pu.age = request.POST.get('age')
                if (request.POST.get('driving_experience') != ''):
                    pu.driving_experience = request.POST.get('driving_experience')
                if (request.POST.get('phone_number') != ''):
                    pu.phone_number = request.POST.get('phone_number')
                if (request.POST.get('email') != ''):
                    pu.email = request.POST.get('email')
                if (request.POST.get('fileInput')):
                    avatar = request.POST.get('fileInput')
                    # 从base64编码的字符串中获取图片数据
                    image_data = avatar.split(",")[1]

                    # 解码图片数据
                    decoded_image_data = base64.b64decode(image_data)
                    # 获取当前的时间，并将其格式化为一个字符串
                    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

                    # 图片文件的路径
                    image_file_path = os.path.join("static", "runData", f"Person_{current_time}.jpg")
                    # 将图片数据写入文件
                    with open(image_file_path, "wb") as image_file:
                        image_file.write(decoded_image_data)
                    pu.photo = "../" + image_file_path

                pu.save()
            return HttpResponse('{"status":"success", "msg":"修改成功！"}', content_type='application/json')
        except Exception as e:
            print(e)
            return HttpResponse('{"status":"failed", "msg":"修改失败！"}', content_type='application/json')
