# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import operator
import math
from .models import News, Forum, UserFav, BrowserHistory, Leave, Classify, UserProfile
from rest_framework import mixins, generics, viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import NewsSerializer, ForumSerializer, ForumSerializer2, SmsSerializer, \
    UserRegSerializer, UserFavSerializer, UserDetailSerializer, UserFavDetailSerializer\
    ,UserBrowserBhistorySerializer, LeaveCreateSerializer, LeaveListSerializer,ClassifySerializer,\
    HotSerializer,UserBrowserBhistorySerializer1

from .filters import NewsFilterSet, ForumFilterSet
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
import random
from rest_framework import status
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.utils import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from utils.sendverificationcode import SendVerificationCode
from utils.translate import Translate

User = get_user_model()

class CustomBackend(ModelBackend):
    """
    用户自定义类
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    wx登陆
    """

    serializer_class = SmsSerializer
    def create(self, request, *args, **kwargs):
        # request.data._mutable = True
        request.query_params._mutable = True
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            from utils.wxlogin import WXLogin
            wx = WXLogin()
            data = wx.get_openid_key(serializer.data['code'])
            a = serializer.data
            a['session_key'] = data['session_key']
            a['openid'] = data['openid']
        except Exception as e:
            print(e)
            a = {'msg', 'wx登陆失败！'}
        return Response(a, status=status.HTTP_201_CREATED)




class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin,  mixins.DestroyModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    用户注册
    """
    # serializer_class = UserRegSerializer
    queryset = User.objects.all()
    # authentication_classes = (JSONWebTokenAuthentication, )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        payload = jwt_payload_handler(user)
        serializer.data["token"] = jwt_encode_handler(payload)
        serializer.data["name"] = user.nick_name if user.nick_name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
       return serializer.save()

    def get_object(self):
        return self.request.user

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        return UserDetailSerializer



class PaginationSet(PageNumberPagination):
    """
    新闻分页类
    """
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

class ClassifySet(mixins.ListModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    """
    list:
    信息分类
    
    retrieve:
    信息分类详情
    """
    queryset = Classify.objects.all()
    serializer_class = ClassifySerializer



class NewsViewSet( generics.ListAPIView, viewsets.ReadOnlyModelViewSet):
    """
    list:
    新闻列表
    retrieve:
    新闻详情
    """
    queryset = News.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        cfrom = self.request.query_params.get('cfrom', None)
        to = self.request.query_params.get('to', None)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if cfrom is not None and to is not None:
                for i in serializer.data:
                    t = Translate(cfrom, to)
                    i['title'] = t.runs(i['title'])
                return self.get_paginated_response(serializer.data)
            else:
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if cfrom is not None and to is not None:
            for i in serializer.data:
                t = Translate(cfrom, to)
                i['title'] = t.runs(i['title'])
            return Response(serializer.data)
        else:
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        new = News.objects.get(id=data['id'])
        new.page_view += 1
        new.save()
        cfrom = self.request.query_params.get('cfrom', None)
        to = self.request.query_params.get('to', None)
        if cfrom is not None and to is not None:
            try:
                t = Translate(cfrom, to)
                data['title'] = t.runs(data['title'])
                data['text'] = t.runs(data['text'])
                return Response(data)
            except:
                pass
        else:
            return Response(data)


    serializer_class = NewsSerializer
    pagination_class = PaginationSet
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)


    # 过滤
    filter_fields = ('classify',)
    # 搜素
    search_fields = ( 'title', 'text', 'label')
    # 排序
    ordering_fields = ('updated_at',)
    # 默认排序
    ordering = ('-updated_at')







class ForumViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
    帖子列表 
    
    retrieve:
    帖子详情
    
    create:
    添加帖子
    
    delete:
    删除帖子
    """
    queryset = Forum.objects.all()
    def create(self, request, *args, **kwargs):
            request.data._mutable = True
            request.query_params._mutable = True
            t = Translate('uy', 'zh')
            request.data['title'] = t.runs(request.data['title']).replace('<br>','')
            request.data['content'] = t.runs(request.data['content']).replace('<br>','')
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        cfrom = self.request.query_params.get('cfrom', None)
        to = self.request.query_params.get('to', None)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if cfrom is not None and to is not None:
                for i in serializer.data:
                    t = Translate(cfrom, to)
                    i['title'] = t.runs(i['title'])
                return self.get_paginated_response(serializer.data)
            else:
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if cfrom is not None and to is not None:
            for i in serializer.data:
                t = Translate(cfrom, to)
                i['title'] = t.runs(i['title'])
            return Response(serializer.data)
        else:
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        cfrom = self.request.query_params.get('cfrom', None)
        to = self.request.query_params.get('to', None)
        if cfrom is not None and to is not None:
            try:
                data = serializer.data
                t = Translate(cfrom, to)
                data['title'] = t.runs(data['title'])
                data['content'] = t.runs(data['content'])
                return Response(data)
            except:
                pass
        else:
            return Response(serializer.data)
    serializer_class = ForumSerializer
    pagination_class = PaginationSet
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('type', 'exist')
    filterset_class = ForumFilterSet
    search_fields = ('title', 'type')
    ordering_fields = ('updated_at',)
    ordering = ('-updated_at')
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action == 'list':
            return [permissions.IsAuthenticated()]
        return []

    def get_serializer_class(self):
        if self.action == 'list':
            return ForumSerializer2
        elif self.action == 'create':
            return ForumSerializer
        return ForumSerializer2


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
    收藏列表 
    
    retrieve:
    收藏详情
    
    create:
    添加收藏
    
    delete:
    删除收藏
    """
    # serializer_class = UserFavSerializer
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


    def get_queryset(self):
        return UserFav.objects.filter(user_id=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        return UserFavDetailSerializer

class UserBrowserHistoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                                mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
    浏览历史列表 

    retrieve:
    浏览历史详情

    create:
    添加浏览历史
    """
    filter_backends = (filters.OrderingFilter,)
    def get_serializer_class(self):
        if self.action == 'list':
            return UserBrowserBhistorySerializer
        elif self.action == 'create':
            return UserBrowserBhistorySerializer1
        return UserBrowserBhistorySerializer
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    ordering_fields = ('created_at',)
    ordering = ('-created_at')
    lookup_field = 'news_id'

    def get_queryset(self):
        return BrowserHistory.objects.filter(user_id=self.request.user)

class UserForumViewSet( mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
    问答列表 

    retrieve:
    问答详情
    """

    filter_backends = (filters.OrderingFilter,)
    serializer_class = ForumSerializer
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    ordering_fields = ('created_at',)
    ordering = ('-created_at')

    def get_queryset(self):
        return Forum.objects.filter(user_id=self.request.user)

class LeaveViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin ,viewsets.GenericViewSet):
    """
    list:
    留言列表 

    retrieve:
    留言详情
    
    create：
    添加留言
    """
    queryset = Leave.objects.all()
    def create(self, request, *args, **kwargs):
            request.data._mutable = True
            request.query_params._mutable = True
            t = Translate('uy', 'zh')
            request.data['content'] = t.runs(request.data['content']).replace('<br>','')
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        cfrom = self.request.query_params.get('cfrom', None)
        to = self.request.query_params.get('to', None)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if cfrom is not None and to is not None:
                for i in serializer.data:
                    t = Translate(cfrom, to)
                    i['content'] = t.runs(i['content'])
                return self.get_paginated_response(serializer.data)
            else:
                return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        if cfrom is not None and to is not None:
            for i in serializer.data:
                t = Translate(cfrom, to)
                i['content'] = t.runs(i['content'])
            return Response(serializer.data)
        else:
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        cfrom = self.request.query_params.get('cfrom', None)
        to = self.request.query_params.get('to', None)
        if cfrom is not None and to is not None:
            try:
                data = serializer.data
                t = Translate(cfrom, to)
                data['content'] = t.runs(data['content'])
                return Response(data)
            except:
                pass
        else:
            return Response(serializer.data)

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('forum',)
    # serializer_class = LeaveSerializer
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    ordering_fields = ('created_at',)
    ordering = ('-created_at')
    def get_serializer_class(self):
        if self.action == 'list':
            return LeaveListSerializer
        elif self.action == 'create':
            return LeaveCreateSerializer
        return LeaveListSerializer


# 推荐算法
class Tjsf(object):
    def __init__(self, user):
        self.user = user
        self.news_id_list = [news.news for news in BrowserHistory.objects.all()]
        self.all_list = {}
        # 统计浏览历史中的用户有多少个浏览记录{userid: count}
        for i in self.news_id_list:
            for j in BrowserHistory.objects.filter(news_id=i):
                if j.user_id in self.all_list.keys():
                    self.all_list[j.user_id] += 1
                else:
                    self.all_list[j.user_id] = 1
    # 计算2个用户的相似度
    def Jaccard(self, userA, userB):
        fengmu = math.sqrt(userA * userB)
        return 1 / fengmu

# sorted(d.items(),key = operator.itemgetter(1))
    def get_users(self):
        # 获取用户相似度最高的三个用户的相似度值
        xiangsidu = {}
        for k, v in self.all_list.items():
            if k != self.user:
                # xiangsidu['用户{}对于{}的相似度'.format(self.user, k)] = self.Jaccard(self.all_list[self.user], v)
                xiangsidu['{},{}'.format(self.user, k)] = self.Jaccard(self.all_list[self.user], v)
        # return xiangsidu
        # print(sorted(xiangsidu.items(), key=operator.itemgetter(1), reverse=True))
        # return sorted(xiangsidu.items(), key=operator.itemgetter(1), reverse=True)[:3]
        return sorted(xiangsidu.keys(), key=operator.itemgetter(1), reverse=True)[:5]

    def get_all_users(self):
        # 根据上面的相似度值获取对应的用户id
        userid = self.get_users()
        userid_list = []
        for i in userid:
            userid_list.append(i.split(',')[1])
        return userid_list

    def get_all_article(self):
        # 获取三个用户的所有浏览历史文章，排除当前用户已经浏览过的文章
        users = self.get_all_users()
        articles =[]
        now_use_article = []
        for i in users:
            for j in BrowserHistory.objects.filter(user_id=i):
                articles.append(j.news_id)

        for a in BrowserHistory.objects.filter(user_id=self.user):
            now_use_article.append(a.news_id)
        for b in now_use_article:
            if b in articles:
                articles.remove(b)
            else:
                articles.append(b)
        if articles:
            return articles[:5]
        else:
           return [i.id for i in News.objects.all().order_by('-page_view')[:5]]



class HotViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
    留言列表 
    """

    def list(self, request, *args, **kwargs):
        t = Tjsf(user=UserProfile.objects.get(username=request.user).id)
        b = []
        for i in t.get_all_article():
            a = {}
            a['id'] = i
            a['title'] = News.objects.get(id=i).title
            b.append(a)
        return Response({'hot': b})

    serializer_class = HotSerializer
    # authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)