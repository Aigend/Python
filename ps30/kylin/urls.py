"""kylin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from kylin import views as kylin_views

urlpatterns = [
    # 实际环境中，为了站点的安全性，我们一般不能将管理后台的url随便暴露给他人，不能用/admin/这么简单的路径
    path('admin/', admin.site.urls),

    path('mysite/', include('mysite.urls')),  # 调试使用

    path('', kylin_views.show_front_view),  # 前端使用
    path('log', kylin_views.download_log),  # log接口
    path('info', kylin_views.show_info),  # info接口

    path('kylin/oss_control/', include('oss_control.urls')),  # oss控制接口
    path('kylin/oss/', include('oss_welkin.urls')),  # kafka云端接口
    path('kylin/cloud/', include('oss_welkin.urls')),  # kafka云端接口
    path('kylin/bms/', include('bms.urls')),  # bms接口
    path('kylin/acdc/', include('acdc.urls')),  # acdc接口
    path('kylin/matrix/', include('matrix.urls')),  # matrix接口
    path('kylin/cgw/', include('cgw.urls')),  # 车载cgw接口
    path('kylin/aec/', include('aec.urls')),  # ai接口
    path('kylin/liquid/', include('liquid.urls')),  # 水冷接口
    path('kylin/meter/', include('meter.urls')),  # 电表接口
    path('kylin/pcu_meter/', include('pcu_meter.urls')),  # PCU 电表接口
    path('kylin/temp_humi_sensor/', include('sensor.urls')),  # CMC 温湿度接口
    path('kylin/pcu_temp_humi_sensor/', include('pcu_sensor.urls')),  # PCU 温湿度接口
    path('kylin/sct/', include('sct.urls')),  # SCT接口
    path('kylin/icc/', include('icc.urls')),  # ICC接口
    path('kylin/pdu/', include('pdu.urls')),  # PDU接口
    path('kylin/plc/', include('plc.urls')),  # plc接口
    # path('kylin/cloud/', include('cloud.urls')),  # cloud接口
    path('kylin/detect/', include('detect.urls')),  # 绝缘检测板接口
    path('kylin/mpc/', include('mpc.urls'))  # 绝缘检测板接口
]
