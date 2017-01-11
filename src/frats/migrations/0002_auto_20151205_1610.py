# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('frats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frat',
            name='members',
            field=models.ManyToManyField(related_name='members_of_frat', through='frats.Member', to=settings.AUTH_USER_MODEL),
        ),
    ]
