# _*_ encoding:utf-8 _*_
import  json

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout#认证登录注册
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View#以类的形式实现 需要继承djang的view
from django.contrib.auth.hashers import make_password  #把注册的时候把密码存成密文
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm
from .forms import UserInfoForm,AddImageForm,AddFileForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course,Lesson,CourseResource,Video
from .models import Banner

#用邮箱登录
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):#用来检查密码
                return user
        except Exception as e:
            return None
#邮箱验证激活
class AciveUserView(View):
    def get(self, request, active_code):#把链接后面的验证码提取出来
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email#从验证码表里找出邮箱
                user = UserProfile.objects.get(email=email)#去用户表匹配，找出注册的用户进行激活
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form":register_form, "msg":"用户已经存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False#表名用户还未激活
            user_profile.password = make_password(pass_word)
            user_profile.save()

            #写入欢迎注册消息
            #这是给我的信息的提示
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册在线学习网"
            user_message.save()

            send_register_email(user_name, "register")##此处是为了进行邮箱验证码验证
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form":register_form})


class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))
#教师登录
class TeacherLoginView(View):
    def get(self,request):
        return render(request,'teacher_login.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        teacher = Teacher.objects.filter(teacher_name=username).first()

        if teacher:
            request.session['tid'] = teacher.id
            request.session['tname'] = username
            if teacher.password == password:
                course_list = Course.objects.filter(teacher_id = teacher.id)
                # print(course_list)
                return render(request, 'teacher_dao/list.html', {
                    'course_list':course_list,
                })
            else:
                return render(request, 'teacher_login.html', {
                    'password_error': "密码错误",
                })
        else:
            return render(request, 'teacher_login.html', {
                'user_error': "用户名错误",
            })

#教师注销
class TeacherLogOutView(View):
    def get(self,request):
        teacherid = request.session.get('tid', 0)

        tname = request.session.get('tname', "")

        if teacherid:
            del request.session['tid']
        if tname:
            del request.session['tname']
        return redirect(reverse('teacher_list'))
#教师登录列表主页
class TeacherListView(View):
    def get(self,request):
        teacherid = request.session.get('tid', 0)

        teacher = Teacher.objects.filter(id=int(teacherid)).first()

        if teacher:
            course_list = Course.objects.filter(teacher_id=teacher.id)
            return render(request, 'teacher_dao/list.html', {
                'course_list': course_list,
            })
        else:
            return render(request, 'teacher_dao/list.html')
#删除教师课程
class DeleteSourceView(View):
    def get(self,request,cid):
        con = Course.objects.filter(id=int(cid)).delete()

        return HttpResponse(con[0])
#教师操作章节列表
class ZhangJieView(View):
    def get(self,request,cid):
        #章节列表
        lessonlist = Lesson.objects.filter(course_id=int(cid))
        #课程资源
        sourcelist = CourseResource.objects.filter(course_id = int(cid))
        cour = Course.objects.filter(id=int(cid)).first()
        cname = cour.name
        return render(request,'teacher_dao/zhangjie.html',{
            'lessonlist':lessonlist,
            'sourcelist':sourcelist,
            'cname':cname,
            'cid':cid
        })

#添加章节
class Add_ZhangjieView(View):
    def get(self,request,cid):
        return render(request,'teacher_dao/add_zhangjie.html',{
            'cid':cid
        })
class Add_ZhangjieView2(View):
    def post(self,request):
        name = request.POST.get("name", "")
        shichang = request.POST.get("shichang", "")
        cid = request.POST.get("cid", "")
        course = Course.objects.filter(id = int(cid)).first()
        less = Lesson()
        less.course = course
        less.name = name
        less.learn_times = shichang
        less.save()
        return HttpResponseRedirect('/teacherzhangjie/%s'%(cid))
#删除章节
class DeleteZhangjieView(View):
    def get(self,request,lid):
        con = Lesson.objects.filter(id=int(lid)).delete()
        return HttpResponse(con[0])

#添加资源 AddFileForm
class Add_ZiyuanView(View):
    def get(self,request,cid):
        return render(request,'teacher_dao/add_source.html',{
            'cid':cid,
        })
class Add_ZiyuanView2(View):
    def post(self,request):
        file_form = AddFileForm(request.POST, request.FILES)
        # print(type(file_form))
        if file_form.is_valid():
            print('ok')
            download = file_form.cleaned_data['download']
            name = request.POST.get("name", "")
            cid = request.POST.get("cid", "")
            cour = Course.objects.filter(id=int(cid)).first()
            coursesource = CourseResource()
            coursesource.course = cour
            coursesource.name = name
            coursesource.download = download
            coursesource.save()
            return HttpResponseRedirect('/teacherzhangjie/%s'%(cid))

#删除资源
class DeleteZiyuanView(View):
    def get(self,request,sid):
        con = CourseResource.objects.filter(id=int(sid)).delete()
        return HttpResponse(con[0])

#添加教师课程
class AddCourseView(View):
    def get(self,request):
        return render(request,'teacher_dao/add_teacher_course.html')
    def post(self,request):
        image_form = AddImageForm(request.POST, request.FILES)
        if image_form.is_valid():

            image = image_form.cleaned_data['image']
            name = request.POST.get("name", "")
            jianjie = request.POST.get("jianjie", "")
            message = request.POST.get("message", "")

            tid = request.session.get('tid')
            teacher = Teacher.objects.filter(id = tid).first()
            # print(type(teacher))
            # print(type(teacher.org))
            course = Course()
            course.course_org = teacher.org
            course.name = name
            course.desc = jianjie
            course.detail = message
            course.teacher = teacher
            course.degree = 'cj'
            course.image = image
            course.save()
            return HttpResponseRedirect('/teacherlist/')

#章节中的视频资源
class SourceListView(View):
    def get(self,request,lid):
        # print(sid)
        sourcelist = Video.objects.filter(lesson_id = int(lid))
        less = Lesson.objects.filter(id=int(lid)).first()
        print(less)
        zname = less.name
        return render(request,'teacher_dao/videolist.html',{
            'sourcelist':sourcelist,
            "zname":zname,
            'lid':lid,
        })

#添加视频资源
class AddVideoView(View):
    def get(self,request,lid):
        return render(request,'teacher_dao/add_video.html',{
            'lid':lid
        })
class AddVideoView2(View):
    def post(self,request):
        name = request.POST.get("name", "")
        shichang = request.POST.get("shichang", "")
        url = request.POST.get("url", "")
        lid = request.POST.get("lid", "")
        less = Lesson.objects.filter(id=int(lid)).first()
        print(less)
        video = Video()
        video.lesson = less
        video.name = name
        video.learn_times = shichang
        video.url = url
        video.save()
        return HttpResponseRedirect('/sourcelist/%s'%(lid))

#删除视频
class DeleteVideoView(View):
    def get(self,request,vid):
        con = Video.objects.filter(id=int(vid)).delete()
        return HttpResponse(con[0])

#登录
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})
    def post(self, request):
        login_form = LoginForm(request.POST)
        # print(login_form)
        if login_form.is_valid():#用来验证前端的数据是否出现错误
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            user = authenticate(username=user_name, password=pass_word)#该部位没有匹配到数据

            if user is not None:
                if user.is_active:
                    login(request, user)
                    #把用户id存进session
                    request.session['uid'] = user.id
                    # print(user.id)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg":"用户未激活！"})
            else:
                return render(request, "login.html", {"msg":"用户名或密码错误！"})
        else:
            return render(request, "login.html", {"login_form":login_form})

#忘记密码
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form":forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form":forget_form})

#密码重置
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")

class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email":email, "msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email":email, "modify_form":modify_form})


class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')



class UpdatePwdView(View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, "update_email")

        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改个人邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            "user_courses":user_courses
        })


class MyFavOrgView(LoginRequiredMixin, View):
    """
    我收藏的课程机构
    """
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            "org_list":org_list
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    """
    我收藏的授课讲师
    """
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list":teacher_list
        })


class MyFavCourseView(LoginRequiredMixin, View):
    """
    我收藏的课程
    """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            teacher = Course.objects.get(id=course_id)
            course_list.append(teacher)
        return render(request, 'usercenter-fav-course.html', {
            "course_list":course_list
        })


class MymessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id).order_by("-add_time")

        #用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        #对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            "messages":messages
        })


class IndexView(View):
    #慕学在线网 首页
    def get(self, request):
        #取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs
        })


def page_not_found(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def page_error(request):
    #全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response