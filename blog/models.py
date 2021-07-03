# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import timezone

from django.db import models

# Create your models here.
class Blog(models.Model):
    text = models.CharField(max_length=1000, blank=False, null=False)
    user = models.ForeignKey(User)
    likes = models.IntegerField(default=0, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.localtime(timezone.now()))
    updated_date = models.DateTimeField(default=timezone.localtime(timezone.now()), blank=True, null=True)
    blog_name = models.CharField(max_length=100, blank=False, null=False)
    
    def __str__(self):
        return "blog:{}".format(self.pk)
        
class Comments(models.Model):
    text = models.CharField(max_length=1000, blank=False, null=False)
    date = models.DateTimeField(default=timezone.localtime(timezone.now()))
    blog = models.ForeignKey(Blog, related_name="comments")
    user = models.ForeignKey(User, related_name="comments", default='10')
    
    def __str__(self):
        return "comments:{}".format(self.pk)
    
class ReportedBlogs(models.Model):
    blog = models.ForeignKey(Blog, related_name="reported_blog")
    reason = models.CharField(max_length=250, null=False, blank=False)
    user = models.ForeignKey(User, related_name="reported_blog", default='10')
    
    def __str__(self):
        return "reported_blog:{}".format(self.pk)

    
    
