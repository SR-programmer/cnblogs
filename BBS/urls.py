"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views
from django.views.static import serve
from BBS import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # 路由分发的本质
    # url(r'^index1/',([
    #     url(r'^index1_1/',([],None,None)),
    #     url(r'^index1_2/',([],None,None)),
    #     url(r'^index1_3/',([],None,None)),
    #
    #
    #                  ],None,None)),
    url(r'^register/', views.register),
    url(r'^login/', views.login),

    # 图片验证码相关路由
    url(r'^get_code/',views.get_code),

    # 主页
    url(r'^home/',views.home),
    # 注销
    url(r'^logout/',views.logout),
    # 修改密码
    url(r'^set_password/',views.set_password),

    # 手动暴露后端文件夹资源
    url(r'^media/(?P<path>.*)',serve,{"document_root":settings.MEDIA_ROOT}),
    # 手动暴露后端文件资源的时候 一定要慎重
    # url(r'^app01/(?P<path>.*)',serve,{"document_root":settings.MEDIA_ROOT1})


    # 文章点赞点踩功能
    url(r'^up_or_down/',views.up_or_down),

    # 文章评论功能
    url(r'^comment/',views.comment),


    # 后台管理
    url(r'^backend/',views.backend),
    # 后台添加文章
    url(r'^add_article/',views.add_article),
    # 文本编辑器上传的图片功能
    url(r'^upload_img/',views.upload_img),


    # 修改用户头像
    url(r'^edit_avatar/',views.edit_avatar),

    # 个人站点
    url(r'^(?P<username>\w+)/$',views.site),
    # 侧边栏筛选功能
    # url(r'^(?P<username>\w+)/category/(?P<param>\d+)/',views.site),
    # url(r'^(?P<username>\w+)/tag/(?P<param>\d+)/',views.site),
    # url(r'^(?P<username>\w+)/archive/(?P<param>.*)/',views.site),  # 2018-2
    # 合成一条的url
    url(r'^(?P<username>\w+)/(?P<condition>category|tag|archive)/(?P<param>.*)/', views.site),

    # 文章详情页
    url(r'^(?P<username>\w+)/article/(?P<article_id>\d+)/',views.article_detail)

]
