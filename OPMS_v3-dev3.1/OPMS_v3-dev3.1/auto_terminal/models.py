from django.db import models


# Create your models here.
######################################
# 车辆终端
######################################
class AutoTerminalInfo(models.Model):
    car_owner = models.CharField(verbose_name='驾驶员', max_length=30,default='')
    car_number = models.CharField(verbose_name='车牌号', max_length=30)
    fatigue_driving = models.IntegerField(verbose_name='疲劳驾驶次数')
    dangerous_driving = models.IntegerField(verbose_name='危险驾驶次数')
    front_collision = models.IntegerField(verbose_name='前车碰撞预警次数')
    add_time = models.DateTimeField(verbose_name='添加时间')

    class Meta:
        verbose_name = '车辆终端表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.car_number
