# _*_ encoding:utf-8 _*_
import random
from django.shortcuts import render
from django.views.generic.base import View
from .models import Node,Topic
#用来制作分页
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
class CommunView(View):
    def get(self,request):
        #取出节点
        all_node = Node.objects.all()
        # 取出话题
        all_topic = Topic.objects.all()
        #话题总数
        nums = all_topic.count()

        #推荐话题随机选择三个
        hot_topic = random.sample(list(all_topic),3)
        # print(request.session.get('uid', 0))#取出用户id
        # hot_topic = all_topic.order_by("-click_nums")[:3]  # 按照点击数排名
        #取出选择的节点
        node_id = request.GET.get('node', "")
        if node_id:
            #从话题里面找出某个节点的所有数据
            all_topic = all_topic.filter(topic_node_id=int(node_id))

        #按照最新或者最热进行排序
        sort = request.GET.get('sort', "")
        if sort:
            #安添加时间取最新
            if sort == "addtime":
                all_topic = all_topic.order_by("-add_time")
                #按点击数为最热
            elif sort == "clicknum":
                all_topic = all_topic.order_by("-click_num")

        # 对话题进行分页
        try:
            #get page不用管，可以取到
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        #5代表的是5个数据一页
        p = Paginator(all_topic, 3, request=request)
        topics = p.page(page)

        return render(request,"shequ.html",{
            'all_node':all_node,
            'all_topic':topics,
            "nums":nums,
            "node_id":node_id,
            "sort":sort,
            "hot_topic":hot_topic,
        })