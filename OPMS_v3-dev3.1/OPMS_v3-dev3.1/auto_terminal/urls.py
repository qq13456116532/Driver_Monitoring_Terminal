"""
User app
"""
from django.urls import path

from auto_terminal.views import AutoTerminalView, EditAutoTerminalView, DeleteAutoTerminalView, AddAutoTerminalView

app_name = 'auto_terminal'

urlpatterns = [
    # 首页
    path('', AutoTerminalView.as_view(), name='list'),

    path('auto/edit', EditAutoTerminalView.as_view(), name='edit'),
path('auto/delete', DeleteAutoTerminalView.as_view(), name='delete'),
path('auto/add', AddAutoTerminalView.as_view(), name='add'),

]


