# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import CourseListView, CourseInfoView2,CourseDetailView, CourseInfoView, CourseTestView,CommentsView, AddComentsView,CourseVideoView

urlpatterns = [
    #课程列表页
    url(r'^list/$', CourseListView.as_view(), name="course_list"),

    #课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),

    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    url(r'^info2/$', CourseInfoView2.as_view(), name="course_info2"),
    #课程测试
    url(r'^test/(?P<cid>\d+)/$', CourseTestView.as_view(), name="course_test"),

    #课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name="course_comments"),

    #课程视频
    url(r'video/(?P<video_id>\d+)/$', CourseVideoView.as_view(), name='course_video'),

    #添加课程评论
    url(r'^add_comment/$', AddComentsView.as_view(), name="add_comment"),

]