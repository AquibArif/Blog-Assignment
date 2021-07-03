# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-07-02 08:56
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('likes', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime(2021, 7, 2, 8, 56, 4, 992677, tzinfo=utc))),
                ('updated_date', models.DateTimeField(blank=True, default=datetime.datetime(2021, 7, 2, 8, 56, 4, 992747, tzinfo=utc), null=True)),
                ('blog_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 7, 2, 8, 56, 4, 993489, tzinfo=utc))),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='ReportedBlogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=250)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reported_blog', to='blog.Blog')),
            ],
        ),
    ]