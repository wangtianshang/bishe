# _*_ encoding:utf-8 _*_
from django.db import models
from datetime import datetime
from users.models import UserProfile

# Create your models here.
#节点表
class Node(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"节点名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"节点"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



#话题表
class Topic(models.Model):
    #该话题属于哪个用户
    topic_uid = models.IntegerField(default=0,verbose_name=u"用户")
    topic_node = models.ForeignKey(Node,verbose_name=u"所属节点", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"话题名")
    content = models.TextField(max_length=1000,verbose_name=u"话题内容")
    click_num = models.IntegerField(default=0,verbose_name=u"点击数")
    #层级默认为0表示是话题
    floor = models.IntegerField(default=0,verbose_name=u"层级")
    number = models.IntegerField(default=0,verbose_name=u"评论数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    image = models.ImageField(upload_to="topic/%Y/%m", verbose_name=u"话题封面", max_length=100)

    class Meta:
        verbose_name = u"话题"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PingLun(models.Model):
    pinglun_topic = models.ForeignKey(Topic,verbose_name=u"所属话题", null=True, blank=True)#相当于话题id
    cengji = models.IntegerField(default=1,verbose_name=u"层级")
    mubiao_user = models.IntegerField(default=1,verbose_name=u"话题所属用户")#相当于话题用户id
    pinglun_text = models.CharField(max_length=300,verbose_name=u"评论内容")
    pinglun_user = models.IntegerField(verbose_name=u"评论者")#相当于评论用户id
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = u"话题评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name