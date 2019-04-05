# _*_ encoding:utf-8 _*_
import random
from django.shortcuts import render,HttpResponse
from django.views.generic.base import View
from .models import Node,Topic,PingLun
from users.models import UserProfile
#用来制作分页
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
#社区之我的话题
class MyTopicView(View):
    def get(self,request):
        # 取出节点
        all_node = Node.objects.all()
        # 取出用户的话题
        all_topic = Topic.objects.filter(topic_uid=request.session.get('uid', 0))
        print(all_topic)
        # 话题总数
        nums = all_topic.count()

        # 推荐话题从全部话题中随机选择三个
        hot_topic = random.sample(list(Topic.objects.all()), 3)
        print(request.session.get('uid', 0))  # 取出用户id
        # hot_topic = all_topic.order_by("-click_nums")[:3]  # 按照点击数排名
        # 取出选择的节点
        node_id = request.GET.get('node', "")
        if node_id:
            # 从话题里面找出某个节点的所有数据
            all_topic = all_topic.filter(topic_node_id=int(node_id))

        # 按照最新或者最热进行排序
        sort = request.GET.get('sort', "")
        if sort:
            # 安添加时间取最新
            if sort == "addtime":
                all_topic = all_topic.order_by("-add_time")
                # 按点击数为最热
            elif sort == "clicknum":
                all_topic = all_topic.order_by("-click_num")

        # 对话题进行分页
        try:
            # get page不用管，可以取到
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 5代表的是5个数据一页
        p = Paginator(all_topic, 3, request=request)
        topics = p.page(page)

        return render(request, "my_shequ.html", {
            'all_node': all_node,
            'all_topic': topics,
            "nums": nums,
            "node_id": node_id,
            "sort": sort,
            "hot_topic": hot_topic,
        })
#社区
class CommunView(View):

    #get方法解决的是所有的话题
    def get(self,request):
        #取出节点
        all_node = Node.objects.all()
        # 取出话题
        all_topic = Topic.objects.all()
        #话题总数
        nums = all_topic.count()
        #属于某个用户的话题话题
        my_topic = Topic.objects.filter(topic_uid=request.session.get('uid', 0))

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
            "my_topic":my_topic,
        })

#话题详情
class Topic_detailView(View):
    def get(self,request,topic_id):

        topic_xiang = Topic.objects.get(id=int(topic_id))
        # print(topic_xiang.topic_uid)#打印用户id
        topic_xiang.click_num+=1
        topic_xiang.save()
        return render(request,'huati_text.html',
                      {
                        "topic_xiang":topic_xiang,
                      })
#添加话题
class Topic_sendView(View):
    def get(self,request):
        return render(request,'topic_add.html')


#增加评论
class TopicAddView(View):
    """
    用户添加话题评论
    """
    def post(self, request):
        image = ""
        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        if request.session.get('uid'):
            image = UserProfile.objects.get(id=request.session.get('uid')).image  # 取出用户头像路径
        userid = request.POST.get("userid", 0)#用户id
        huatiid = request.POST.get("huatiid", 0)#话题id
        comments = request.POST.get("comments", "")#评论内容
        # print(userid)##读出来的id是字符串
        # print(huatiid)##读出来的id是字符串
        # print(comments)#这个是写入的数据
        if int(huatiid) > 0 and comments:
            topic_pinglun = PingLun()
            huati = Topic.objects.get(id=int(huatiid))
            topic_pinglun.pinglun_topic = huati
            topic_pinglun.mubiao_user = userid
            topic_pinglun.pinglun_text = comments
            topic_pinglun.pinglun_user = request.user.id
            topic_pinglun.mubiao_user_name = request.user
            topic_pinglun.image = image
            topic_pinglun.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')