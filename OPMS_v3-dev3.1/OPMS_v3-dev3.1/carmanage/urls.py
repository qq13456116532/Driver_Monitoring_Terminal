
from django.urls import path

from carmanage.views import CarManageView, EditCarView, DeleteCarView, AddCarView

app_name = 'carmanage'

urlpatterns = [
    # 删除
    path('myuser/delete', DeleteCarView.as_view(), name='delete'),
    # 汽车及终端管理页面
    path('myuser/list', CarManageView.as_view(), name='carmanage'),
    # 用户编辑页面
    path('myuser/edit', EditCarView.as_view(), name='edit'),
    # 用户添加页面
    path('myuser/add', AddCarView.as_view(), name='add')
]
