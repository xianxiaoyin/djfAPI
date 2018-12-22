# conding:utf8
"""
过滤，模糊查询
"""
from django_filters import rest_framework as filters
from .models import News, Forum

class NewsFilterSet(filters.FilterSet):
    # min_price = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    # max_price = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    # 模糊查询
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    class Meta:
        model = News
        fields = ['title']

class ForumFilterSet(filters.FilterSet):
    # min_price = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    # max_price = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    # 模糊查询
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    class Meta:
        model = Forum
        fields = ['title']