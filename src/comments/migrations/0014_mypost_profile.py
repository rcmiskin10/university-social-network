# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0013_mypost_frat'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypost',
            name='profile',
            field=models.ForeignKey(related_name='profile_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
