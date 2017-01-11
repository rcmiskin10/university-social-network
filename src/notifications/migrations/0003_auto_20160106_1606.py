# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20160106_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='action',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(related_name='reciepient_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(related_name='sender_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
