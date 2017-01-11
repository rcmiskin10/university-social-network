# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_auto_20151214_2159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='html',
        ),
        migrations.AddField(
            model_name='syllabus',
            name='html',
            field=models.TextField(null=True, blank=True),
        ),
    ]
