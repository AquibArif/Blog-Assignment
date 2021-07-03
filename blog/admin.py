# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from.models import *

# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ['pk','user', 'blog_name', 'text', 'likes', 'updated_date']
    search_fields = ('user__pk','user__email', 'blog_name')
    
admin.site.register(Blog, BlogAdmin)

class commentsAdmin(admin.ModelAdmin):
    list_display = ["pk", "user", "text","date","blog"]
    search_fields = ("blog__blog_name", "blog__pk", "user__email", "user__pk")
    
admin.site.register(Comments, commentsAdmin)

class ReportedBlogsAdmin(admin.ModelAdmin):
    list_display= ["blog", "reason", "user"]
    search_fields = ("blog__blog_name", "blog__pk", "user__email", "user__pk")
    
admin.site.register(ReportedBlogs, ReportedBlogsAdmin)
