"""
URL configuration for pre_sales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from user.views import account, userinfo, sales, multi, chart, knowledge, workreport
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('', account.login, name='login'),
    # path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    # 登录
    path('login/', account.login),
    path('logout/', account.logout),
    path('image/code/', account.image_code),

    # 用户管理
    path('user/list/', userinfo.userinfo_list),
    path('user/add/', userinfo.userinfo_add),
    path('user/<int:nid>/edit/', userinfo.userinfo_edit),
    path('user/<int:nid>/del/', userinfo.userinfo_del),
    path('user/<int:nid>/reset/', userinfo.userinfo_reset),

    # 售前文档管理
    path('sales/list/', sales.sales_list),
    path('sales/add/', sales.sales_add),
    path('sales/delete/', sales.sales_delete),
    path('sales/edit/', sales.sales_edit),
    path('sales/detail/', sales.sales_detail),

    # 资料上传
    path('document/upload/', multi.multi_upload),
    path('document/list/', multi.multi_list),
    path('document/add/', multi.multi_add),

    # 数据统计
    path('chart/list/', chart.chart_list),
    path('chart/bar/', chart.chart_bar),

    # 知识库
    path('knowledge/list/', knowledge.knowledge_list),

    # 工作周报
    path('work/list/', workreport.workreport_list)
]
