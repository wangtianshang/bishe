# _*_ encoding:utf-8 _*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView#这样可以不用写view函数直接跳转到前台页面
import xadmin
from django.views.static import serve#处理静态位置文件

from users.views import LogoutView, LoginView, RegisterView, AddCourseView,AciveUserView, TeacherListView,ForgetPwdView, ResetView, ModifyPwdView,TeacherLoginView,TeacherLogOutView,ZhangJieView,SourceListView,DeleteSourceView,Add_ZhangjieView,Add_ZiyuanView,AddVideoView,Add_ZhangjieView2,Add_ZiyuanView2,AddVideoView2,DeleteZhangjieView,DeleteZiyuanView,DeleteVideoView
from users.views import IndexView
from community.views import CommunView
from organization.views import OrgView
from MxOnline.settings import MEDIA_ROOT


#IndexView.as_view()把类转换成view函数
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),

    url('^logout/$', LogoutView.as_view(), name="logout"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', AciveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    #教师操作模块
    url('^teacherlogin/$', TeacherLoginView.as_view(), name="teacher_login"),
    url('^teacherlogout/$', TeacherLogOutView.as_view(), name="teacher_logout"),
    url('^teacherlist/$', TeacherListView.as_view(), name="teacher_list"),
    url('^add_teacher_course/$', AddCourseView.as_view(), name="add_teacher_course"),
    #删除课程
    url('^del_source/(?P<cid>.*)/$', DeleteSourceView.as_view(), name="delsource"),

    #章节操作
    url('^add_zhangjie/(?P<cid>.*)/$', Add_ZhangjieView.as_view(), name="add_zhangjie"),
    url('^add_zhangjie2/$', Add_ZhangjieView2.as_view(), name="add_zhangjie2"),
    url('^del_zhangjie/(?P<lid>.*)/$', DeleteZhangjieView.as_view(), name="delzhangjie"),
    url('^add_ziyuan/(?P<cid>.*)/$', Add_ZiyuanView.as_view(), name="add_ziyuan"),
    url('^add_ziyuan2/$', Add_ZiyuanView2.as_view(), name="add_ziyuan2"),
    url('^del_ziyuan/(?P<sid>.*)/$', DeleteZiyuanView.as_view(), name="delziyuan"),
    url('^teacherzhangjie/(?P<cid>.*)/$', ZhangJieView.as_view(), name="zhangjie"),
    url('^sourcelist/(?P<lid>.*)/$', SourceListView.as_view(), name="sourcelist"),

    #添加视频
    url('^add_video/(?P<lid>.*)/$', AddVideoView.as_view(), name="add_video"),
    url('^add_video2/$', AddVideoView2.as_view(), name="add_video2"),
    url('^del_video/(?P<vid>.*)/$', DeleteVideoView.as_view(), name="delvideo"),

    #话题配置
    url(r'^topic/', include('community.urls', namespace="topic")),

    #课程机构url配置
    url(r'^org/', include('organization.urls', namespace="org")),

    #课程相关url配置
    url(r'^course/', include('courses.urls', namespace="course")),


    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$',  serve, {"document_root":MEDIA_ROOT}),

    # url(r'^static/(?P<path>.*)$',  serve, {"document_root":STATIC_ROOT}),

    #课程相关url配置
    url(r'^users/', include('users.urls', namespace="users")),

    #富文本相关url
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
]

#全局404页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'