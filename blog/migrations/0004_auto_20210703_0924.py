# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-07-03 09:24
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_auto_20210702_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportedblogs',
            name='user',
            field=models.ForeignKey(default='10', on_delete=django.db.models.deletion.CASCADE, related_name='reported_blog', to=settings.AUTH_USER_MODEL),
        ),
    ]
