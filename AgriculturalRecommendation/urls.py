#-*- coding:utf-8 -*-
"""AgriculturalRecommendation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from AgriculturalRecommendation.settings import MEDIA_ROOT
from django.views.static import serve
from recommend_templates.views import NewsViewSet, ForumViewSet, SmsCodeViewSet, \
    UserViewSet, UserFavViewSet, UserBrowserHistoryViewSet, UserForumViewSet, LeaveViewSet, \
    ClassifySet
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

router = DefaultRouter()
router.register(r'news', NewsViewSet, base_name='news')
router.register(r'forums', ForumViewSet, base_name='forum')
router.register(r'leave', LeaveViewSet , base_name='leave')
router.register(r'code', SmsCodeViewSet, base_name='code')
router.register(r'users', UserViewSet, base_name='user')
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')
router.register(r'userforums', UserForumViewSet, base_name='userforum')
router.register(r'browserhistory', UserBrowserHistoryViewSet, base_name='browserhistory')
router.register(r'classfiy', ClassifySet, base_name='classfiy')


urlpatterns = [
    # 后台
    url(r'^admin/', include(admin.site.urls)),
    # drf
    url(r'^login/', obtain_jwt_token),
    url(r'^docs/', include_docs_urls(title='个人新闻')),
    url(r'^', include(router.urls)),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
