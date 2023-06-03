from django.test import TestCase

from driver.models import DriverInfo
from django.test import TransactionTestCase


class DriverInfoTestCase(TransactionTestCase):
    def test_create_multiple_drivers(self):
        # 使用 for 循环创建多个驾驶员实例
        for i in range(10):
            driver = DriverInfo.objects.create(
                name=f"Driver {i}",
                gender="M",
                license_number=f"License {i}",
                age=30,
                driving_experience=5,
                phone_number="123456789",
                email=f"driver{i}@example.com",
                fatigue_driving_count=0,
                dangerous_driving_count=0,
                front_collision_warning_count=0,
                update_time="2022-01-01"
            )
            driver.save()
        # 在测试中添加以下 assert 语句来检查是否成功地创建了 10 个驾驶员实例
        self.assertEqual(DriverInfo.objects.count(), 10)
