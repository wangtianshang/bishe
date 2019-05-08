# -*- coding: utf-8 -*-
import json
from django.shortcuts import render,redirect
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q

from .models import Course, CourseResource,Video,CourseXuanzeTest,CoursePanduanTest,CourseTiankongTest,TestSorce
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
from organization.models import Teacher
# Create your views here.

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        #课程搜索
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))

        #课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        #对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 12, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses":courses,
            "sort":sort,
            "hot_courses":hot_courses
        })


class CourseVideoView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        video = Video.objects.get(id=video_id)
        course = video.lesson.course
        all_resource = CourseResource.objects.filter(course=course)

        # 查询用户是否已经关联了该数据
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            # 如果没有则写入数据库
            my_course = UserCourse(user=request.user, course=course)
            my_course.save()

        # 该同学还学过
        user_courses = UserCourse.objects.filter(course=course)  # 获取“用户课程”表里面该课程的所有记录
        user_ids = [user_course.user.id for user_course in user_courses]  # 获取学过该课程的所有用户id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # 获取这些用户学过的课程记录
        course_ids = [user_course.id for user_course in all_user_courses]  # 获取这些课程的id
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]  # 根据点击量取出5个

        return render(request, 'course-play.html', {
            'course': course,
            'all_resource': all_resource,
            'relate_courses': relate_courses,
            'video': video,
        })

class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        teacher = Teacher.objects.get(id = course.teacher_id)

        #增加课程点击数
        course.click_nums += 1
        course.save()

        #是否收藏课程
        has_fav_course = False
        #是否收藏机构
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_coures = Course.objects.filter(tag=tag)[:1]
        else:
            relate_coures = []
        return render(request, "course-detail.html", {
            "course":course,
            "relate_coures":relate_coures,
            "has_fav_course":has_fav_course,
            "has_fav_org":has_fav_org,
            "teacher":teacher
        })

class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        #查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_cousers = UserCourse.objects.filter(course=course)
        user_ids = [user_couser.user.id for user_couser in user_cousers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程id
        course_ids = [user_couser.course.id for user_couser in all_user_courses]
        #获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course":course,
            "course_resources":all_resources,
            "relate_courses":relate_courses
        })


#课程测试
class CourseTestView(View):
    def get(self,request,cid):
        course = Course.objects.get(id=int(cid))
        #选择题
        xuanzelist = CourseXuanzeTest.objects.filter(course=int(cid))
        #判断题
        panduanlist = CoursePanduanTest.objects.filter(course=int(cid))
        #填空题
        tiankonglist = CourseTiankongTest.objects.filter(course=int(cid))

        uid = request.session['uid']
        #分数
        score = TestSorce.objects.filter(course=int(cid),user=int(uid)).first()
        if not score:
            sc = 0
        else:
            sc = score.sorce
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-test.html", {
            "course": course,
            'cid':cid,
            "course_resources": all_resources,
            'xuanzelist':xuanzelist,
            'panduanlist':panduanlist,
            'tiankonglist':tiankonglist,
            'score':sc
        })

class CourseInfoView2(View):
    def post(self,request):
        # 用来记录正确的数量
        sum = 0
        cid = request.POST.get("cid", "")
        xuanzelist = CourseXuanzeTest.objects.filter(course=int(cid))
        # 这是提交的选择题答案
        lists = request.POST.getlist("myarray")
        ans = []
        for i in xuanzelist:
            ans.append(i.answer)

        for i in range(len(ans)):
            if lists:
                if lists[i]:
                    if ans[i] == lists[i]:
                        sum+=1
                else:
                    continue
            else:
                continue
        #判断题模块
        panduanlist = CoursePanduanTest.objects.filter(course=int(cid))
        # 这是提交的判断题答案
        lists2 = request.POST.getlist("myarray2")
        ans2 = []
        for i in panduanlist:
            ans2.append(i.answer)
        for i in range(len(ans2)):
            if lists2:
                if lists2[i]:
                    if ans2[i] == lists2[i]:
                        sum+=1
                else:
                    continue
            else:
                continue

        #填空题模块
        tiankonglist = CourseTiankongTest.objects.filter(course=int(cid))

        # 这是提交的填空题答案
        lists3 = request.POST.getlist("myarray3")
        print(lists3)
        ans3 = []
        for i in tiankonglist:
            ans3.append(i.answer)
        print(ans3)
        # for i in range(len(ans3)):
        #     if lists3:
        #         if lists3[i]:
        #             if ans3[i] == lists3[i]:
        #                 sum += 1
        #         else:
        #             continue
        #     else:
        #         continue
        sum = sum*10

        #修改分数
        tsco = TestSorce.objects.filter(course=int(cid),user=int(request.session['uid'])).first()
        tsco.sorce = sum
        tsco.save()

        data = {}
        data['msg'] = sum
        data['status'] = 'success'
        return HttpResponse(json.dumps(data))


class CommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all().order_by("-id")
        return render(request, "course-comment.html", {
            "course":course,
            "course_resources":all_resources,
            "all_comments":all_comments
        })


class AddComentsView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        # print(type(course_id))##读出来的id是字符串
        # print(comments)#这个是写入的数据
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()

            return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加失败"}', content_type='application/json')