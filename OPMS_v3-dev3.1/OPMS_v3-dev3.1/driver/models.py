from django.db import models

# Create your models here.
######################################
# 驾驶员
######################################
class DriverInfo(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    license_number = models.CharField(verbose_name="驾驶证编号" , max_length=20)
    age = models.IntegerField(verbose_name="年龄")
    driving_experience = models.IntegerField(verbose_name="驾龄")
    phone_number = models.CharField(verbose_name="手机号",max_length=20)
    email = models.EmailField(verbose_name="邮箱")
    photo = models.CharField(verbose_name="人脸识别照片", max_length=255,default="")
    fatigue_driving_count = models.IntegerField(verbose_name="疲劳驾驶次数")
    dangerous_driving_count = models.IntegerField(verbose_name="危险驾驶次数")
    front_collision_warning_count = models.IntegerField(verbose_name="前车碰撞预警次数")
    update_time = models.DateTimeField(verbose_name="更新时间")
    class Meta:
        verbose_name = '驾驶员表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name