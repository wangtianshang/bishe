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
from .views import CommunView,Topic_detailView,Topic_sendView,MyTopicView,TopicAddView,Topic_sendView2


#IndexView.as_view()把类转换成view函数
urlpatterns = [
    url(r'^list/$', CommunView.as_view(), name="topic_list"),
    url(r'^mylist/$', MyTopicView.as_view(), name="my_topic_list"),
    url(r'^detail/(?P<topic_id>\d+)/$', Topic_detailView.as_view(), name="topic_detail"),
    url(r'^send/$', Topic_sendView.as_view(), name="topic_send"),
    url(r'^send2/$', Topic_sendView2.as_view(), name="topic_send2"),
    url(r'^add_comment/$', TopicAddView.as_view(), name="pinglun_add"),

]

