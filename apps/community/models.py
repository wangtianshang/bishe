# _*_ encoding:utf-8 _*_
from django.db import models
from datetime import datetime
# Create your models here.
class Node(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"节点名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"节点"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Topic(models.Model):
    topic_node = models.ForeignKey(Node,verbose_name=u"所属节点", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"话题名")
    content = models.TextField(max_length=100,verbose_name=u"话题内容")
    click_num = models.IntegerField(default=0,verbose_name=u"点击数")
    number = models.IntegerField(default=0,verbose_name=u"评论数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"话题"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name