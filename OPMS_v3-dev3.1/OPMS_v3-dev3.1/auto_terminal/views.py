import datetime
import os
import tempfile
import time
import zipfile
from io import BytesIO
from pathlib import Path

import xlwt
from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.utils import timezone
from django.views import View

from pure_pagination import PageNotAnInteger, Paginator

from auto_terminal.models import AutoTerminalInfo
from carmanage.models import Carmanage


######################################
# 首页
######################################
class AddAutoTerminalView(View):
    def post(self,request):
        driver = request.POST.get('driver')
        license = request.POST.get('license')
        auto = AutoTerminalInfo(car_owner=driver, car_number=license)
        auto.dangerous_driving = 0
        auto.fatigue_driving = 0
        auto.front_collision = 0
        auto.add_time = datetime.datetime.now()

        auto.save()
        return HttpResponse('{"status":"success", "msg":"增加成功！"}', content_type='application/json')



class DeleteAutoTerminalView(View):
    def post(self, request):
        driver = AutoTerminalInfo.objects.get(id=int(request.POST.get('id')))
        driver.delete()
        return HttpResponse('{"status":"success", "msg":"删除成功！"}', content_type='application/json')


class AutoTerminalView(View):
    def get(self, request):
        # 页面选择
        web_chose_left_1 = 'carend'
        web_chose_left_2 = 'list'
        web_chose_middle = ''

        title = '车辆终端'
        # 搜索的条件
        start_time = request.GET.get("start_time", "")
        stop_time = request.GET.get("stop_time", "")
        owner = request.GET.getlist("owner", "")
        export_data = ""
        action = request.GET.get("action", "")
        carends = AutoTerminalInfo.objects.all().order_by("id")
        carlist = AutoTerminalInfo.objects.values_list()

        car_owners = carends.values_list("id", flat=True)
        if action != "":
            if (action == "search") or (action == "export_search"):
                if start_time != "":
                    carends = carends.filter(add_time__gte=start_time)
                if stop_time != "":
                    carends = carends.filter(add_time__lte=stop_time)
                if owner != "":
                    carends = carends.filter(id__in=owner)
            if action == "export_search":
                export_data = carends
            if (action == "export_all"):
                export_data = carends

            if (action == "export_search") or (action == "export_all"):
                if(action == "export_search" and owner=='' and start_time=='' and stop_time==''):
                    return HttpResponse('{"status":"failed", "msg":"没有选择条件！"}', content_type='application/json')

                # 创建 excel
                new_excel = xlwt.Workbook(encoding='utf-8')
                excel_page = new_excel.add_sheet(u'终端报警')

                # 插入第一行标题
                excel_page.write(0, 0, u'id')
                excel_page.write(0, 1, u'驾驶员')
                excel_page.write(0, 2, u'车牌号')
                excel_page.write(0, 3, u'疲劳驾驶次数')
                excel_page.write(0, 4, u'危险驾驶次数')
                excel_page.write(0, 5, u'前车碰撞预警次数')
                excel_page.write(0, 6, u'添加时间')

                # 初始行
                excel_row = 1
                # 创建zip文件
                zip_file_path = "static/runData/waringData/car_terminal.zip"
                zipf = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
                if (export_data != '') and export_data:
                    for each in export_data:

                        id_excel = each.id
                        car_owner_excel = each.car_owner
                        car_number_excel = each.car_number
                        carmanage = Carmanage.objects.all().filter(license_plate=car_number_excel).first()
                        terminal_number = carmanage.terminal_number
                        dir_name = "static/runData/waringData/" + terminal_number + "/"

                        folders = ["danger", "distance", "fatigue", "face"]
                        for folder in folders:
                            folder_path = Path(dir_name + folder)
                            if folder_path.exists():  # 检查文件夹是否存在
                                # 获取文件夹下所有的 jpg 文件，按修改时间排序，最新的文件在最前面
                                jpg_files = sorted(folder_path.glob('*.jpg'), key=os.path.getmtime, reverse=True)
                                if jpg_files:  # 如果文件夹下有 jpg 文件
                                    latest_jpg = jpg_files[0]  # 取最新的 jpg 文件
                                    # 将文件添加到压缩文件中，文件名为 "each_id.jpg"，并保留在相应的文件夹中
                                    zipf.write(latest_jpg, arcname=f"{folder}/{each.id}.jpg")

                        fatigue_driving_excel = each.fatigue_driving
                        dangerous_driving_excel = each.dangerous_driving
                        front_collision_excel = each.front_collision
                        add_time_excel = each.add_time

                        # 定义时间格式
                        time_style = 'YYYY/MM/DD HH:mm'
                        style = xlwt.XFStyle()
                        style.num_format_str = time_style

                        # 写数据
                        excel_page.write(excel_row, 0, id_excel)
                        excel_page.write(excel_row, 1, car_owner_excel)
                        excel_page.write(excel_row, 2, car_number_excel)
                        excel_page.write(excel_row, 3, fatigue_driving_excel)
                        excel_page.write(excel_row, 4, dangerous_driving_excel)
                        excel_page.write(excel_row, 5, front_collision_excel)
                        excel_page.write(excel_row, 6, add_time_excel, style)

                        # 行数加1
                        excel_row += 1

                    # 导出文件
                    time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())
                    filename = '终端报警_' + time_now + '.xls'

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


        # 过滤
        # carends = AutoTerminalInfo.objects.filter(belong=1).filter(is_public=True)
        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(carends, 17, request=request)

        # 分页处理后的 QuerySet
        carends = p.page(page)

        context = {
            'web_chose_left_1': web_chose_left_1,
            'web_chose_left_2': web_chose_left_2,
            'web_chose_middle': web_chose_middle,
            'title': title,
            'carends': carends,
            'car_owners': car_owners
        }
        return render(request, 'car_end/carendlist.html', context=context)


######################################
# 编辑
######################################
class EditAutoTerminalView(View):
    def post(self, request):
        print("看一下request： ", request.POST)
        try:
            id = request.POST.get('id', '')
            if id != '':
                pu = AutoTerminalInfo.objects.get(id=int(id))
                pu.dangerous_driving = request.POST.get('dangerous_driving', '')
                pu.fatigue_driving = request.POST.get('fatigue_driving', '')
                pu.front_collision = request.POST.get('front_collision', '')
                pu.save()
            return HttpResponse('{"status":"success", "msg":"修改成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"failed", "msg":"修改失败！"}', content_type='application/json')
