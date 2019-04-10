# _*_ encoding:utf-8 _*_
import random
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.views.generic.base import View
from .models import Node,Topic,PingLun,HuiFu,HuiFuHuiFu
from users.models import UserProfile
from operation.models import UserMessage
#用来制作分页
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UploadImageForm
# Create your views here.
#社区之我的话题
class MyTopicView(View):
    def get(self,request):
        # 取出节点
        all_node = Node.objects.all()
        # 取出用户的话题
        all_topic = Topic.objects.filter(topic_uid=request.session.get('uid', 0))
        # print(all_topic)
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
        # 取出所有话题
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
        all_node = Node.objects.all()
        return render(request,'topic_add.html',{
            "all_node":all_node
        })

    def post(self,request):
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            name = request.POST.get("name", "")
            jiedian = request.POST.get("jiedian", "其他")
            jiedian_node = Node.objects.filter(name=jiedian)
            message = request.POST.get("message", "")
            # image = request.POST.get("image", "")
            topic = Topic()
            topic.topic_uid = request.user.id
            topic.topic_node = jiedian_node[0]
            topic.name = name
            topic.content = message
            topic.image = image
            topic.save()
        return HttpResponse('ok')

#快速添加话题
class Topic_sendView2(View):
    def post(self,request):
        name = request.POST.get('name', '')
        message = request.POST.get('message', '')
        jiedian_node = Node.objects.filter(name="其他")
        image = "topic/2019/04/other.jpg"
        topic = Topic()
        topic.topic_uid = request.user.id
        topic.topic_node = jiedian_node[0]
        topic.name = name
        topic.content = message
        topic.image = image
        topic.save()
        return render(request,"shequ.html")

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
            topic_xiang = Topic.objects.get(id=int(huatiid))
            topic_xiang.number += 1
            topic_xiang.save()

            user_message = UserMessage()
            user_message.user = topic_pinglun.mubiao_user
            user_message.message = "有人评论了你"
            user_message.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')


class HuiFuAddView(View):
    def post(self,request):
        image = ""
        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        if request.session.get('uid'):
            image = UserProfile.objects.get(id=request.session.get('uid')).image  # 取出用户头像路径
        pinglun_id = request.POST.get("pinglun_id")
        pinglun_user = request.POST.get("pinglun_user")
        pinglun_user_name = request.POST.get("pinglun_user_name")

        comments = request.POST.get("comments")
        #判断自己不能评论自己
        if str(request.user) == pinglun_user_name:
            return HttpResponse('{"status":"fail", "msg":"不能自己回复自己的评论"}', content_type='application/json')

        if int(pinglun_id) > 0:
            topic_huifu = HuiFu()
            suoshu_pinglun = PingLun.objects.get(id=int(pinglun_id))

            topic_huifu.huifu_pinglun = suoshu_pinglun
            topic_huifu.cengji = 2
            topic_huifu.pinglun_text = comments
            topic_huifu.mubiao_user = pinglun_user#这个是被回复着，也就是评论者id
            topic_huifu.mubiao_user_name = pinglun_user_name
            topic_huifu.huifu_user = request.user.id#这个是回复者id
            topic_huifu.huifu_user_name = request.user
            topic_huifu.image = image
            topic_huifu.save()
            print(pinglun_user_name)
            print(pinglun_user)
            user_message = UserMessage()
            user_message.user = pinglun_user
            user_message.message = "有人回复了你的评论"
            user_message.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
                return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')

class NewHuiFuAddView(View):
    def post(self,request):
        image = ""
        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        if request.session.get('uid'):
            image = UserProfile.objects.get(id=request.session.get('uid')).image  # 取出用户头像路径
        huifu_id = request.POST.get("huifu_id")
        huifu_user = request.POST.get("huifu_user")
        huifu_user_name = request.POST.get("huifu_user_name")
        comments = request.POST.get("comments")
        # 判断自己不能回复自己
        if str(request.user) == huifu_user_name:
            return HttpResponse('{"status":"fail", "msg":"不能自己回复自己"}', content_type='application/json')

        if int(huifu_id) > 0:
            topic_huifu = HuiFuHuiFu()
            suoshu_huifu = HuiFu.objects.get(id=int(huifu_id))
            print(suoshu_huifu)
            topic_huifu.huifu_huifu = suoshu_huifu
            topic_huifu.cengji = 3
            topic_huifu.text = comments
            topic_huifu.mubiao_user = huifu_user  # 这个是该条回复的所有者
            topic_huifu.mubiao_user_name = huifu_user_name#所有者名字
            topic_huifu.huifu_user = request.user.id  # 这个是回复者id（即是回复那条回复的人）
            topic_huifu.huifu_user_name = request.user#回复者名字
            topic_huifu.image = image
            topic_huifu.save()

            user_message = UserMessage()
            user_message.user = huifu_user
            user_message.message = "有人回复了你的回复"
            user_message.save()
            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')
