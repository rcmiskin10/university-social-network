# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0019_coursenote'),
        ('comments', '0009_auto_20160101_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypost',
            name='course',
            field=models.ForeignKey(blank=True, to='course.Course', null=True),
        ),
    ]
