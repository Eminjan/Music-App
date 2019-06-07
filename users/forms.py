#!/usr/bin/env
# -*-coding:utf-8-*-
# @Author  : E🚀M

from django import forms
from .models import UserProfile

class RegisterForm(forms.Form):
    """
    注册表单
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=6)


class LoginForm(forms.Form):
    """
    登录验证表单
    """
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=6)


class ModifyPwdForm(forms.Form):
    """
    修改密码
    """
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


class UploadAvatarForm(forms.ModelForm):
    """
    上传修改头像
    """
    class Meta:
        model = UserProfile
        fields = ['avatar']


class UpdateUserProfileForm(forms.Form):
    """
    修改个人资料
    """
    username = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    birthday = forms.DateField(required=True)
    address = forms.CharField(required=False)

from captcha.fields import CaptchaField
# 激活时验证码实现
class ActiveForm(forms.Form):
    # 激活时不对邮箱密码做验证
    # 应用验证码 自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


