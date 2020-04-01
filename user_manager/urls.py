"""user_manager URL Configuration （用户管理器URL配置）

#“urlpatterns”列表将url路由到视图。详情请参阅:
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/

Examples:例子:
Function views （功能视图）
    1. Add an import:  from my_app import views 添加导入:从my_app导入视图
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')添加一个URL到urlpatterns: URL (r'^$'，视图)。家,name = '家')
    Class-based views（基于类的观点）
    1. Add an import:  from other_app.views import Home  添加导入:来自other_app。视图导入回家
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home') 添加一个URL到urlpatterns: URL (r'^$'， home .as_view()， name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include 从django.conf导入include()函数。url导入url，包括包括另一个URLconf
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls')) 添加一个URL到urlpatterns: URL (r'^blog/'，包括('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login.html$', views.login),
    url(r'^logout.html$', views.logout),
    url(r'^index.html$', views.index),
    url(r'^classes.html$', views.handle_class),
    url(r'^add_classes.html$', views.handle_add_classes),
    url(r'^edit_classes.html$', views.handle_edit_classes),
    url(r'^registered.html$', views.registered),
    url(r'^mother_set.html$', views.mother_set),
    url(r'^registered.html$', views.registered),
    url(r'^student.html$', views.handle_student),
    url(r'^teacher.html$', views.handle_teacher),
    url(r'^test.html$', views.test),
    url(r'^page.html$', views.page),
    url(r'^add_student.html$', views.add_student),
    url(r'^edit_student.html$', views.edit_student),
    url(r'^Error_pages.html$', views.Error_pages),
    url(r'^add_teacher.html$', views.add_teacher),
    url(r'^edit_teacher-(\d+).html$', views.edit_teacher),
]
