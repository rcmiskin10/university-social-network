# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_schedule_club'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='choice',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
