from django.db import models

from driver.models import DriverInfo


# Create your models here.
class Carmanage(models.Model):
    license_plate = models.CharField(verbose_name="车牌号",max_length=20, unique=True)
    terminal_number = models.CharField(verbose_name="车载终端编号",max_length=20, unique=True)
    operating_route = models.CharField(verbose_name="运营路线",max_length=100)
    company = models.CharField(verbose_name="所属公司",max_length=100)
    driver_id = models.ForeignKey(DriverInfo, on_delete=models.CASCADE)
    class Meta:
        verbose_name = '车辆及终端表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name