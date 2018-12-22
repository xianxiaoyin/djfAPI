# _*_ coding:utf-8 _*_

from django import forms

from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class RegisterForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误！'})


class ForumForm(forms.Form):
    title = forms.CharField(required=True)
    types = forms.CharField(required=True)
    content = forms.CharField(required=True)
    status = forms.CharField(required=True)
