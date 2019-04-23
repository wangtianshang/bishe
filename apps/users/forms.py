# -*- coding: utf-8 -*-
__author__ = 'bobby'
__date__ = '2016/10/29 23:01'
#用from做表单验证
from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile
from courses.models import Course

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)#指定是否可以为空和最小长度


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})#生成的验证码   可以定制错误信息

#忘记密码
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

#修改密码
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

#添加课程图片
class AddImageForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']

