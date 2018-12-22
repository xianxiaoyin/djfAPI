# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, News, Forum


class UserProfileAdmin(UserAdmin):
    list_display = ['username', 'nick_name', 'education', 'expertise', 'field', 'third_party']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'classify', 'label', 'text', 'created_at', 'updated_at', 'exist']


class ForumAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'content', 'page_view', 'compliment_num', 'collect_num', 'status',
                    'updated_at', 'created_at', 'exist']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Forum, ForumAdmin)
