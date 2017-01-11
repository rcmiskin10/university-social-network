# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0007_auto_20151229_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypost',
            name='main',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
