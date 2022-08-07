"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

"""
    1.re_path 的使用
    2.namespace和name的使用
"""
from django.contrib import admin
from django.urls import path, re_path, include
# from django.conf.urls import handler400, handler403, handler404, handler500

from mysite import views

extractpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('home/', views.index, name='index'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', admin.site.urls),
    # path('index/', views.IndexView.as_view(), name='index'),
    # path("find1/<int:std>", views.find1, name="find1"),
    # path('find2/<str:std>/<str:name>', views.find2, name="find2"),
    # path('<slug:slugStr>', views.slugStr, name='slugStr'),
    # path('<uuid:uu>/<int:numb>', views.uu, name='uu'),
    # path('<path:home>', views.home, name='home'),

    # path('myapp/', include(extractpatterns), name='index'),
    # path('myapp/', include((extractpatterns, 'myapp')), name='index'),
    # path('myapp/', include('myapp.urls', namespace="myapp")),

]

handler404 = views.page_not_found #改动2
handler500 = views.page_error