from django.core.paginator import PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render
from django.views import View
######################################
# Django 模块
######################################
from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.sessions.models import Session

from auto_terminal.models import AutoTerminalInfo
from carmanage.models import Carmanage
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

from driver.models import DriverInfo


# Create your views here.
######################################
# 用户管理页面
######################################
class CarManageView(View):
    def get(self, request):
        # 页面选择
        web_chose_left_1 = 'carmanage'
        web_chose_left_2 = 'manage'
        web_chose_middle = ''
        title = '车辆及终端管理'
        cars = Carmanage.objects.all()
        # 搜索
        keyword = request.GET.get('keyword', '')
        if keyword != '':
            cars = cars.filter(Q(license_plate__icontains=keyword) | Q(terminal_number__icontains=keyword))
        cars_nums = cars.count()
        # 判断页码
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 对取到的数据进行分页，记得定义每页的数量
        p = Paginator(cars, 17, request=request)

        # 分页处理后的 QuerySet
        cars = p.page(page)
        drivers = DriverInfo.objects.all()
        print("看一下driver：  ")
        print(drivers.all().values_list())
        autos = AutoTerminalInfo.objects.all()
        license_plates = autos.values_list('car_number', flat=True)
        context = {
            'web_chose_left_1': web_chose_left_1,
            'web_chose_left_2': web_chose_left_2,
            'web_chose_middle': web_chose_middle,
            'title': title,
            'cars': cars,
            'cars_nums': cars_nums,
            'drivers': drivers,
            'license_plates': license_plates,
        }
        return render(request, 'cars/cars_manage.html', context=context)


######################################
# 编辑
######################################
class EditCarView(View):
    def post(self, request):
        print("看一下request： ", request.POST)
        try:
            id = request.POST.get('id', '')
            if id != '':
                pu = Carmanage.objects.get(id=int(id))
                if (request.POST.get('license_plate') != ''):
                    pu.license_plate = request.POST.get('license_plate', pu.license_plate)
                if (request.POST.get('terminal_number') != ''):
                    pu.terminal_number = int(request.POST.get('terminal_number', pu.terminal_number))
                if (request.POST.get('operating_route') != ''):
                    pu.operating_route = int(request.POST.get('operating_route', pu.operating_route))
                if (request.POST.get('company') != ''):
                    pu.company = int(request.POST.get('company', pu.company))
                if (request.POST.get('driver_id') != ''):
                    if Carmanage.objects.filter(driver_id=int(request.POST.get('driver_id', pu.driver_id))):
                        return HttpResponse('{"status":"failed", "msg":"该驾驶员已经有了其他车辆！"}',
                                            content_type='application/json')
                    pu.driver_id = DriverInfo.objects.get(id=int(request.POST.get('driver_id', pu.driver_id)))
                    # 汽车
                    auto_terminal = AutoTerminalInfo.objects.get(car_number=pu.license_plate)
                    #驾驶员
                    driver = DriverInfo.objects.get(id = int(request.POST.get('driver_id', pu.driver_id)))
                    if(auto_terminal.fatigue_driving>driver.fatigue_driving_count):
                        auto_terminal.fatigue_driving -= driver.fatigue_driving_count
                    else:
                        auto_terminal.fatigue_driving = 0
                    if(auto_terminal.dangerous_driving>driver.dangerous_driving_count):
                        auto_terminal.dangerous_driving -= driver.dangerous_driving_count
                    else:
                        auto_terminal.dangerous_driving =0
                    if(auto_terminal.front_collision>driver.front_collision_warning_count):
                        auto_terminal.front_collision -= driver.front_collision_warning_count
                    else:
                        auto_terminal.front_collision =0
                    auto_terminal.save()
                pu.save()
            return HttpResponse('{"status":"success", "msg":"修改成功！"}', content_type='application/json')
        except Exception as e:
            return HttpResponse('{"status":"failed", "msg":"修改失败！"}', content_type='application/json')


######################################
# 删除
######################################
class DeleteCarView(View):
    def post(self, request):
        car = Carmanage.objects.get(id=int(request.POST.get('id')))
        car.delete()
        # 添加操作记录
        # op_record = UserOperationRecord()
        # op_record.op_user = request.user
        # op_record.belong = 1
        # op_record.status = 1
        # op_record.op_num = int(request.POST.get('id'))
        # op_record.operation = 4
        # op_record.action = "删除汽车及终端：%s  ( %s )" % (car.license_plate, car.terminal_number)
        # op_record.save()

        return HttpResponse('{"status":"success", "msg":"汽车删除成功！"}', content_type='application/json')


######################################
# 添加
######################################
class AddCarView(View):
    def post(self, request):
        license_plate = request.POST.get('license_plate')
        terminal_number = request.POST.get('terminal_number')
        operating_route = request.POST.get('operating_route')
        company = request.POST.get('company')
        driver_id = request.POST.get('driver_id')
        if Carmanage.objects.filter(license_plate=license_plate):
            return HttpResponse('{"status":"failed", "msg":"该车牌号已经被另外的车辆使用！"}',
                                content_type='application/json')
        if Carmanage.objects.filter(terminal_number=terminal_number):
            return HttpResponse('{"status":"failed", "msg":"该车载终端已经被另外的车辆使用！"}',
                                content_type='application/json')
        if Carmanage.objects.filter(driver_id=driver_id):
            return HttpResponse('{"status":"failed", "msg":"该驾驶员已经有了其他车辆！"}',
                                content_type='application/json')

        # 添加用户
        car = Carmanage()
        car.license_plate = license_plate
        car.terminal_number = terminal_number
        car.operating_route = operating_route
        car.company = company
        # driver = DriverInfo.objects.get(id=1)
        try:
            driver = DriverInfo.objects.get(id=driver_id)
            car.driver_id = driver
            car.save()
            # 添加操作记录
            # op_record = UserOperationRecord()
            # op_record.op_user = request.user
            # op_record.belong = 2
            # op_record.status = 1
            # op_record.op_num = car.id
            # op_record.operation = 1
            # op_record.action = "新增车辆 [ %s ]" % car.license_plate
            # op_record.save()
            return HttpResponse('{"status":"success", "msg":"用户添加成功，但未激活，请知悉！"}',
                                content_type='application/json')
        except DriverInfo.DoesNotExist:
            return HttpResponse('{"status": "failed", "msg": "填写的内容不正确，请检查！"}',
                                content_type='application/json')


    # return HttpResponse('{"status":"failed", "msg":"填写的内容不正确，请检查！"}',
    #                         content_type='application/json')
