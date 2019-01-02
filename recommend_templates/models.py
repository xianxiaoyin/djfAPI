# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    """
    扩展用户类
    """
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称', default=u'')
    gender = models.CharField(max_length=10, choices=(('male', u'男'), ('female', u'女')), default=u'')
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m', default='img/default.png')
    birday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    real_name = models.CharField(max_length=20, verbose_name=u'真实姓名', null=True, blank=True, default='')
    education = models.CharField(max_length=20, verbose_name=u'教育经历', null=True, blank=True, default='')
    expertise = models.CharField(max_length=20, verbose_name=u'专业技能', null=True, blank=True, default='')
    field = models.CharField(max_length=20, verbose_name=u'熟悉领域', null=True, blank=True, default='')
    third_party = models.CharField(max_length=20, verbose_name=u'第三方登录', null=True, blank=True, default='')

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.username

class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(verbose_name=u'验证码', max_length=6)
    moblie = models.CharField(verbose_name=u'手机号', max_length=11)
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, null=True)
    class Meta:
        verbose_name = u'短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code

class Classify(models.Model):
    """
    分类
    """
    name = models.CharField(verbose_name='中文名', max_length=20)
    desc = models.CharField(verbose_name='缩写', max_length=10)
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, null=True)
    class Meta:
        verbose_name = u'分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class News(models.Model):
    """
    新闻
    """
    title = models.CharField(verbose_name=u'标题', max_length=50, unique=True)
    url = models.URLField(verbose_name=u'文章url链接', default='')
    classify = models.ForeignKey(Classify, verbose_name=u'分类')
    label = models.CharField(verbose_name=u'标签', max_length=20)
    text = models.TextField(verbose_name=u'内容')
    page_view = models.IntegerField(verbose_name=u'浏览次数', default=0)
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    exist = models.BooleanField(verbose_name=u'状态', default=True)

    class Meta:
        verbose_name = u'新闻'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class BrowserHistory(models.Model):
    """
    用户浏览记录
    """
    user = models.ForeignKey(UserProfile, verbose_name=u'用户id')
    news = models.ForeignKey(News, verbose_name=u'新闻id')
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = u'用户浏览记录'
        verbose_name_plural = verbose_name


class Forum(models.Model):
    """
    用户问答
    """
    type_list = (
        ('jg', '价格'),
        ('fxyc', '分析预测'),
        ('syjs', '实用技术'),
    )
    status_list = (
        ('dhd', '待回答'),
        ('yjj', '已解决'),
    )
    user = models.ForeignKey(UserProfile, verbose_name=u'用户id')
    title = models.CharField(verbose_name=u'帖子标题', max_length=50)
    type = models.CharField(verbose_name=u'帖子分类', max_length=20, choices=type_list)
    content = models.TextField(verbose_name=u'内容')
    page_view = models.IntegerField(verbose_name=u'浏览次数', default=0)
    compliment_num = models.IntegerField(verbose_name=u'点赞数量', default=0)
    collect_num = models.IntegerField(verbose_name=u'收藏数量', default=0)
    status = models.CharField(verbose_name=u'帖子状态', max_length=20, choices=status_list)
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    exist = models.BooleanField(verbose_name=u'状态', default=True)

    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class Leave(models.Model):
    """
    帖子留言
    """
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    forum = models.ForeignKey(Forum, verbose_name=u'帖子')
    content = models.TextField(verbose_name=u'留言')
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = verbose_name


class UserFav(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey(UserProfile, verbose_name=u'用户')
    news = models.ForeignKey(News, verbose_name=u'新闻')
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'news')
    def __str__(self):
        return self.user.username



