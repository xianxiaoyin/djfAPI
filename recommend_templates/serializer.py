# coding:utf8

from rest_framework import serializers
from .models import News, UserProfile, Forum, Leave, Classify
from django.contrib.auth import get_user_model
import re
import datetime
from datetime import timedelta
from AgriculturalRecommendation.settings import REGEX_MOBILE
from .models import VerifyCode, UserFav, BrowserHistory
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

User = get_user_model()

class UserProfileSerialize(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id',)

class ClassifySerializer(serializers.ModelSerializer):
    """
    新闻类的序列化器
    """
    name = serializers.CharField()
    class Meta:
        model = Classify
        fields = ('id', 'name')
        # fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    """
    新闻类的序列化器
    """
    classify = ClassifySerializer()
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = News
        fields = "__all__"




class SmsSerializer(serializers.Serializer):
    """
    用户注册序列化类
    """
    code = serializers.CharField()
    token = serializers.CharField(read_only=True)
    openid = serializers.CharField(read_only=True)
    # class Meta:
    #     model = VerifyCode
    #     fields = ('code',)

class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册序列化类
    """
    code = serializers.CharField(required=True, max_length=6, min_length=4, write_only=True,
                                 error_messages={
                                     "required": "验证码不能为空！",
                                     "blank": "验证码不能为空！",
                                     "max_length": "验证码格式错误！",
                                     "min_length": "验证码格式错误！",
                                 })
    username = serializers.CharField( read_only=True,
                                     allow_blank=False,
                                    validators=[UniqueValidator(queryset=User.objects.all(),
                                                                 message="用于已存在！")])
    password = serializers.CharField(write_only=True,
        style={'input_type': 'password'}
    )
    def validate_code(self, code):
        mobile = self.initial_data["mobile"]
        vcode = VerifyCode.objects.filter(moblie=mobile).order_by("-created_at")
        if vcode:
            five_mintes_ago = datetime.datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            last_code = vcode[0]
            if last_code.created_at < five_mintes_ago:
                raise serializers.ValidationError("验证码过期！")
            if last_code.code != code:
                raise serializers.ValidationError("验证码不匹配！")
            return code
        else:
            raise serializers.ValidationError("未知的验证码！")

    # def validate_password(self, password):
    #     from django.contrib.auth.hashers import make_password
    #     password = self.initial_data["password"]
    #     return make_password(password)



    def validate(self, attrs):
        attrs["username"] = attrs["mobile"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ('username','mobile','code', 'password')


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化器
    """
    image = serializers.ImageField(allow_empty_file=True, use_url=True, allow_null=True )
    def validate_image(self, image):
        if not image:
            return User.objects.get(username=self.instance.username).image
        else:
            return image
    class Meta:
        model = User
        fields = ('mobile','gender', 'nick_name', 'birday', 'image')



class UserFavSerializer(serializers.ModelSerializer):
    """
    用户收藏的序列化器
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = UserFav
        fields = ("user", "news", "id")
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=("user", "news"),
                message="已收藏"
            )
        ]

class UserFavDetailSerializer(serializers.ModelSerializer):
    """
    用户收藏详情的序列化器
    """
    news = NewsSerializer()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = UserFav
        fields = ("user", "news", "id")

class LeaveCreateSerializer(serializers.ModelSerializer):
    """
    Leave类的序列化器
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Leave
        fields = "__all__"

class LeaveListSerializer(serializers.ModelSerializer):
    """
    Leave类的序列化器
    """
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    # forum = ForumSerializer2()
    class Meta:
        model = Leave
        fields = ('id', 'content', 'created_at')

class ForumSerializer(serializers.ModelSerializer):
    """
    Forum类的序列化器
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    title = serializers.CharField(help_text="帖子标题")
    type = serializers.CharField(help_text="帖子类型")
    content = serializers.CharField(help_text="帖子内容")
    class Meta:
        model = Forum
        fields = ('user','title','type','content','id')
        # fields = "__all__"

class ForumSerializer2(serializers.ModelSerializer):
    """
    Forum类的序列化器
    """
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Forum
        fields = ('user','title','id', 'updated_at', 'created_at')
        # fields = "__all__"

class UserBrowserBhistorySerializer(serializers.ModelSerializer):
    """
    用户浏览历史序列化器
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    # news = NewsSerializer()
    class Meta:
        model = BrowserHistory
        fields = ('user', 'news', 'created_at')
        validators = [
            UniqueTogetherValidator(
                queryset=BrowserHistory.objects.all(),
                fields=("user", "news"),
                message="已存在"
            )
        ]







