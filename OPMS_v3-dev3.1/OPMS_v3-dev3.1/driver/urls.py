from django.urls import path

from auto_terminal.views import AutoTerminalView, EditAutoTerminalView
from driver.views import DriverListView, EditDriverView, AddDriverView, DeleteDriverView

app_name = 'driver'

urlpatterns = [
    # 首页
    path('', DriverListView.as_view(), name='list'),
path('driver/delete', DeleteDriverView.as_view(), name='delete'),
    path('driver/edit', EditDriverView.as_view(), name='edit'),
    path('driver/add', AddDriverView.as_view(), name='add'),

]

